import random
import time

import pygame
import numpy as np

pygame.init()

filled_cells = {
    "easy": 30,
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
    for row in range(9):
        row_elements = game_board[row, :].flatten().tolist()
        if not valid_elements(row_elements):
            return False
    return True


def valid_cols(game_board):
    """

    :param game_board:
    :return:
    """

    for col in range(9):
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


def random_solver(game_board):
    """
    TODO:
     - fixme

    :param game_board:
    :return:
    """
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    if game_board[row, col] == 0:
        game_board[row, col] = random.randint(1, 9)
        timeout = 0
        while not valid_board(game_board) and timeout < 10:
            game_board[row, col] = random.randint(1, 9)
            timeout += 1
        if timeout >= 10:
            game_board[row, col] = 0
    return game_board


def init_game_board(difficulty):
    filled = filled_cells[difficulty]
    game_board = np.zeros((9, 9), dtype=int)

    filled_positions = []
    for _ in range(filled):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        filled_positions.append((x, y))

    for x,y in filled_positions:
        game_board[x, y] = random.randint(1, 9)
        while not valid_board(game_board):
            game_board[x, y] = random.randint(1, 9)
    return game_board


def get_sprites(game_board, digits):
    rows, cols = game_board.shape
    sprites = []
    for i in range(rows):
        for j in range(cols):
            game_digit = int(game_board[i][j])
            sprites.append(
                (
                    digits[game_digit],
                    i * 48,
                    j * 48,
                )
            )
    return sprites


def main():
    digit_size = 48
    grid_size = digit_size * 9

    pygame.display.set_caption("PyDOKU")
    window_surface = pygame.display.set_mode((grid_size, grid_size))

    is_running = True

    digits = [pygame.image.load("./assets/{}.png".format(i)) for i in range(10)]
    difficulty = "easy"

    game_board = init_game_board(difficulty)

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        game_board = random_solver(game_board)
        window_surface.fill(pygame.Color("#ffffff"))
        for sprite, x, y in get_sprites(game_board, digits):
            window_surface.blit(sprite, (x, y))
        pygame.display.update()


if __name__ == "__main__":
    main()
