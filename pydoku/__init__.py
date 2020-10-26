import random
import time

import pygame
import numpy as np

pygame.init()

filled_cells = {
    "easy": 75,
    "medium": 20,
    "hard": 10,
    "ai": 0,
}


def no_duplicates(elements):
    """

    >>> no_duplicates([1, 2, 3])
    True
    >>> no_duplicates([])
    True
    >>> no_duplicates([1, 2, 2])
    False

    :param elements:
    :return:
    """
    num_elements = len(elements)
    unique_elements = len(set(elements))
    return num_elements == unique_elements


def less_than_nine(elements):
    """

    >>> less_than_nine([])
    True
    >>> less_than_nine([1, 2, 9])
    True
    >>> less_than_nine([10, 1, 2])
    False

    :param elements:
    :return:
    """
    for el in elements:
        if el > 9:
            return False
    return True


def valid_length(elements):
    """

    >>> valid_length([1 ,2, 3])
    True
    >>> valid_length([])
    True
    >>> valid_length(range(12))
    False

    :param elements:
    :return:
    """
    return len(elements) < 10


def valid_elements(elements):
    """

    >>> valid_elements([0, 0, 0, 0, 0, 0, 0, 0, 0])
    True
    >>> valid_elements([1, 2, 3, 4, 5, 6, 7, 8, 9])
    True
    >>> valid_elements([1, 2, 2, 9, 5, 6, 7, 4, 3])
    False
    >>> valid_elements([10, 2, 8, 9, 5, 6, 7, 4, 3])
    False
    >>> valid_elements([1, 2, 3, 4, 5, 6, 7, 8, 9])
    True

    :param elements:
    :return:
    """
    elements = [element for element in elements if element != 0]
    return (
        no_duplicates(elements) and valid_length(elements) and less_than_nine(elements)
    )


def valid_rows(game_board):
    """
    :param game_board:
    :return:
    """
    rows, _ = game_board.shape
    for row in range(rows):
        row_elements = game_board[row, :].flatten().tolist()
        if not valid_elements(row_elements):
            return False
    return True


def valid_cols(game_board):
    """

    :param game_board:
    :return:
    """
    _, cols = game_board.shape
    for col in range(cols):
        col_elements = game_board[:, col].flatten().tolist()
        if not valid_elements(col_elements):
            return False
    return True


def valid_boxes(game_board):
    for i in range(2):
        for j in range(2):
            box_elements = (
                game_board[3 * i : 3 * (i + 1), 3 * j : 3 * (j + 1)].flatten().tolist()
            )
            if not valid_elements(box_elements):
                return False
    return True


def valid_board(game_board):
    return valid_rows(game_board) and valid_cols(game_board) and valid_boxes(game_board)


def none_empty(game_board):
    """

    >>> none_empty(np.array([[1, 0], [3, 4]]))
    False
    >>> none_empty(np.array([[1, 2], [3, 4]]))
    True

    :param game_board:
    :return:
    """
    return np.all(game_board > 0)


def solved(game_board):
    return valid_board(game_board) and none_empty(game_board)


def find_random_empty_cell(game_board):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    while game_board[row, col] != 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
    return row, col


def find_empty_cell(game_board):
    rows, cols = game_board.shape
    for row in range(rows):
        for col in range(cols):
            if game_board[row, col] == 0:
                return row, col
    raise ValueError("no empty cells.")


def next_value(value):
    """

    >>> next_value(0)
    1
    >>> next_value(1)
    2
    >>> next_value(3)
    4
    >>> next_value(9)
    1

    :param value:
    :return:
    """
    value += 1
    return value % 9


def get_slice(index):
    """

    >>> get_slice(2)
    slice(0, 3, None)
    >>> get_slice(3)
    slice(3, 6, None)
    >>> get_slice(8)
    slice(6, 9, None)

    :param index:
    :return:
    """
    if index < 3:
        return slice(0, 3)
    elif index < 6:
        return slice(3, 6)
    else:
        return slice(6, 9)


def get_box_values(game_board, row, col):
    return set(game_board[get_slice(row), get_slice(col)].flatten().tolist())


def get_valid_values(game_board, position):
    row, col = position
    all_values = set(range(1, 10))
    row_values = set(game_board[row, :].flatten().tolist())
    col_values = set(game_board[:, col].flatten().tolist())
    box_values = get_box_values(game_board, row, col)
    return list(
        all_values.difference(row_values).difference(col_values).difference(box_values)
    )


def find_cells_valid_values(game_board):
    rows, cols = game_board.shape
    valid_values = {}
    for row in range(rows):
        for col in range(cols):
            if game_board[row, col] == 0:
                valid_values[(row, col)] = get_valid_values(game_board, (row, col))
    return valid_values


def solve(game_board, positions_log):
    """
    TODO:
     - this does not solve
    """

    if solved(game_board):
        return game_board, positions_log

    return game_board, positions_log


def init_game_board(difficulty):
    """
    TODO:
     - this creates unsolvable boards
    """
    filled = filled_cells[difficulty]
    game_board = np.zeros((9, 9), dtype=int)

    for _ in range(filled):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        while not get_valid_values(game_board, (x, y)):
            x = random.randint(0, 8)
            y = random.randint(0, 8)
        game_board[x, y] = random.choice(get_valid_values(game_board, (x, y)))
    return game_board


def get_sprites(game_board, digits):
    rows, cols = game_board.shape
    sprites = []
    for row in range(rows):
        for col in range(cols):
            game_digit = int(game_board[row][col])
            sprites.append(
                (
                    digits[game_digit],
                    col * 48,
                    row * 48,
                )
            )
    return sprites


def draw_board(window_surface, game_board, digits):
    window_surface.fill(pygame.Color("#ffffff"))
    for sprite, x, y in get_sprites(game_board, digits):
        window_surface.blit(sprite, (x, y))


def main():
    digit_size = 48
    grid_size = digit_size * 9

    pygame.display.set_caption("PyDOKU")
    window_surface = pygame.display.set_mode((grid_size, grid_size))

    is_running = True

    digits = [pygame.image.load("./assets/{}.png".format(i)) for i in range(10)]
    difficulty = "easy"

    game_board = init_game_board(difficulty)
    positions_log = []

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # game_board, positions_log = solve(game_board, positions_log)

        draw_board(window_surface, game_board, digits)
        pygame.display.update()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
