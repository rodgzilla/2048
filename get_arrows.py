import sys
import tty
import termios
from typing import Union

from move import Move

code_to_move = {
    '\x1b[A': Move.UP,
    '\x1b[B': Move.DOWN,
    '\x1b[C': Move.RIGHT,
    '\x1b[D': Move.LEFT,
    'ass': Move.QUIT,
    'che': Move.CHEAT
}

class _Getch:
    def __call__(self) -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

def get_move() -> Move:
    inkey = _Getch()
    while True:
        k = inkey()
        if k != '':
            break

    print(k)
    # if k not in code_to_move:
    #     return move.STAY

    return code_to_move.get(k, Move.STAY)


if __name__=='__main__':
    for i in range(0, 5):
        print(get_move())
