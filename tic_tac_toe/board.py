import copy

import numpy as np

from tic_tac_toe import errors


def create_board():
    board = np.zeros(shape=(3,3), dtype=str)
    board[:, :] = "-"
    return board


def update_board(board, row, column, mark):
    mark = mark.lower()

    if _check_position_is_unmarked(board, row, column):
        board[row, column] = mark
    else:
        raise errors.MarkedPositionError((row, column))
        
    return board  


def _check_position_is_unmarked(board, row, column):
    return board[row, column] == "-"


def _any_row_has_all_values_equal(board, mark):
    return (board == mark).all(1).any()


def _any_column_has_all_values_equal(board, mark):
    return (board == mark).all(0).any()


def _main_diagonal_all_values_equal(board, mark):
    return (np.diag(board) == mark).all()


def _secondary_diagonal_all_values_equal(board, mark):
    return (np.diag(np.fliplr(board)) == mark).all()


def check_player_is_winner(board, mark):
    return (
        _any_row_has_all_values_equal(board, mark)
        or _any_column_has_all_values_equal(board, mark)
        or _main_diagonal_all_values_equal(board, mark)
        or _secondary_diagonal_all_values_equal(board, mark)
    )

def check_draw(board):
    return (board != "-").all()

