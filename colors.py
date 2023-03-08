RESET = '\033[0m'

def get_color_escape(r, g, b, background = False):
    return '\033[{};2;{};{};{}m'.format(
        48 if background else 38,
        r,
        g,
        b
    )

def hex_color_to_triplet(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    return r, g, b

value_to_background_color = {
    2: '#eee4da',
    4: '#eee1c9',
    8: '#f3b27a',
    16: '#f69664',
    32: '#f77c5f',
    64: '#f75f3b',
    128: '#edd073',
    256: '#edcc62',
    512: '#edc950',
    1024: '#edc53f',
    2048: '#edc22e'
}

value_to_text_color = {
    2: '#776e65',
    4: '#776e65',
    8: '#f9f6f2',
    16: '#f9f6f2',
    32: '#f9f6f2',
    64: '#f9f6f2',
    128: '#f9f6f2',
    256: '#f9f6f2',
    512: '#f9f6f2',
    1024: '#f9f6f2',
    2048: '#f9f6f2'
}

def color_text(text, hex_text_color, hex_background_color):
    text_escape = get_color_escape(
        *hex_color_to_triplet(
            hex_text_color
        )
    )
    background_escape = get_color_escape(
        *hex_color_to_triplet(
            hex_background_color
        ),
        True
    )

    return text_escape + background_escape + text + RESET


def format_cell(n: int, n_spaces: int, display_numbers: bool):
    return color_text(
        (
            ' ' * n_spaces +
            (
                f'{n:^4}' if display_numbers else ' ' * 4
            ) +
            ' ' * n_spaces
        ),
        value_to_text_color[n],
        value_to_background_color[n]
    )

if __name__ == '__main__':
    for (v, background_hex_color), (_, text_hex_color) in zip(
        value_to_background_color.items(),
        value_to_text_color.items(),
    ):
        print(color_text(f'{v:^4}', text_hex_color, background_hex_color))
