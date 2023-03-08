import numpy as np
from itertools import chain, repeat
import os

from move import Move
from result import Result
from get_arrows import get_move
from colors import format_cell

class Board():
    def __init__(
        self,
        empty: bool = False,
        two_prob: float = .9,
        display_zeros: bool = False,
        display_just_merged: bool = True,
        display_new_values: bool = True,
        display_old_values: bool = True,
        display_numbers: bool = True,
        n_spaces: int = 1
    ):
        self.rng = np.random.default_rng()
        self.two_prob = two_prob
        self.display_zeros = display_zeros
        self.n_spaces = n_spaces
        self.board = np.zeros((4, 4), dtype = int)
        self.display_just_merged = display_just_merged
        self.display_new_values = display_new_values
        self.display_old_values = display_old_values
        self.display_numbers = display_numbers
        self.just_merged = np.zeros((4, 4), dtype = bool)
        self.new_values = np.zeros((4, 4), dtype = bool)
        self.old_values = np.ones((4, 4), dtype = bool)
        self.n_moves = 0
        self.score = 0
        self.number_to_display_string = {
            2 ** i: format_cell(2 ** i, n_spaces, self.display_numbers)
            for i in range(1, 12)
        }

        if not empty:
            value_pos = self._get_random_empty_cell_pos(self.board, 2)
            initial_values = self._get_random_new_values(2)
            self.board[
                value_pos[:, 0],
                value_pos[:, 1]
            ] = initial_values
            self.new_values[
                value_pos[:, 0],
                value_pos[:, 1]
            ] = True

    def _get_empty_cell_pos(self, board: np.ndarray) -> np.ndarray:
        return np.array(
             np.where(
                board == 0
             )
        ).T

    def _get_random_empty_cell_pos(
        self,
        board: np.ndarray,
        n: int = 1
    ) -> np.ndarray:
        empty_cell_pos = self._get_empty_cell_pos(board)
        indices = self.rng.choice(
            empty_cell_pos.shape[0],
            n,
            replace = False
        )

        return empty_cell_pos[indices]

    def _get_random_new_values(self, n: int = 1):
        return (
            self.rng.choice(
                2, # choose from [0, 1],
                n, # n values to draw
                p = [
                    self.two_prob,      # probability of 2
                    1. - self.two_prob  # probability of 4
                ]
            ) +
            1  # [0, 1] -> [1, 2]
        ) * 2  # [1, 2] -> [2, 4]

    def move_up(self, board: np.ndarray) -> bool:
        something_moved = False
        just_merged = np.zeros((4, 4), dtype = bool)
        new_values = np.zeros((4, 4), dtype = bool)
        old_values = board != 0
        # old_values = np.ones((4, 4), dtype = bool)
        # For each row
        for row_idx, row in enumerate(board):
            # for each cell
            for col_idx, v in enumerate(row):
                # if cell is empty, do nothing
                if v == 0:
                    continue

                # if the cell is not empty, we go up its column
                last_free_row = None
                merge_happened = False
                for row_dest_idx in range(row_idx - 1, -1, -1):
                    v_dest = board[row_dest_idx, col_idx]
                    if v_dest == 0:
                        last_free_row = row_dest_idx
                    elif v_dest == v:
                        if just_merged[row_dest_idx, col_idx]:
                            break
                        board[row_dest_idx, col_idx] = 2 * v
                        self.score += 2 * v
                        board[row_idx, col_idx] = 0
                        just_merged[row_dest_idx, col_idx] = True
                        something_moved = True
                        merge_happened = True
                        break
                    else:
                        break

                if not merge_happened and last_free_row is not None:
                    board[last_free_row, col_idx] = v
                    board[row_idx, col_idx] = 0
                    something_moved = True

        if something_moved:
            new_cell_pos = self._get_random_empty_cell_pos(board)
            new_cell_val = self._get_random_new_values()
            board[
                new_cell_pos[:, 0],
                new_cell_pos[:, 1]
            ] = new_cell_val
            new_values[
                new_cell_pos[:, 0],
                new_cell_pos[:, 1]
            ] = True
            old_values = ~(just_merged | new_values)

        return something_moved, board, just_merged, new_values, old_values

    def move(self, m: Move):
        board = np.copy(self.board)
        if m == Move.DOWN:
            board = board[::-1]
        elif m == Move.LEFT:
            board = board.T
        elif m == Move.RIGHT:
            board = board[:, ::-1].T

        (
            something_moved,
            board,
            just_merged,
            new_values,
            old_values
        ) = self.move_up(board)

        if not something_moved:
            return False

        if m == Move.DOWN:
            board = board[::-1]
            just_merged = just_merged[::-1]
            new_values = new_values[::-1]
            old_values = old_values[::-1]
        elif m == Move.LEFT:
            board = board.T
            just_merged = just_merged.T
            new_values = new_values.T
            old_values = old_values.T
        elif m == Move.RIGHT:
            board = board.T[:, ::-1]
            just_merged = just_merged.T[:, ::-1]
            new_values = new_values.T[:, ::-1]
            old_values = old_values.T[:, ::-1]

        self.board = board
        self.just_merged = just_merged
        self.new_values = new_values
        self.old_values = old_values
        self.n_moves += 1

        return something_moved

    def __repr__(self):
        display_mask = np.zeros_like(self.board, dtype = bool)

        # if        display_just_merged: bool = True,
        # display_new_values: bool = True,
        # display_old_values: bool = True

        if self.display_old_values:
            display_mask |= self.old_values

        if self.display_new_values:
            display_mask |= self.new_values

        if self.display_just_merged:
            display_mask |= self.just_merged

        if not self.display_zeros:
            display_mask &= (self.board != 0)

        row_strs = [
            (
                '|' +
                '|'.join(
                    (
                        self.number_to_display_string[x]
                        if mask_v else
                        ' ' * (2 * self.n_spaces + 4)
                    )
                    for x, mask_v in zip(row, mask_row)
                ) +
                '|'
            )
            for row, mask_row in zip(self.board, display_mask)
        ]
        row_strs = list(chain(
            *zip(
                repeat(
                    '-' * (2 * self.n_spaces + 5) * 4
                ),
                row_strs + ['']
            )
        ))[:-1]

        return (
            f'Moves: {self.n_moves:^5d}   Score: {self.score:^7}\n' +
            '\n'.join(row_strs)
        )


def main():
    board = Board(
        display_just_merged = True,
        display_new_values = True,
        display_old_values = True,
        display_numbers = True
    )
    m = Move.STAY
    while True:
        os.system('clear')
        if m == Move.CHEAT:
            print(board.board)
        print(board, '\n\n')
        m = get_move()
        if m == Move.QUIT:
            break

        if m == Move.CHEAT or m == Move.STAY:
            continue

        board.move(m)


if __name__ == '__main__':
    main()
