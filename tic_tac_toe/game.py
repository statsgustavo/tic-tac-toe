from typing import Dict

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


def _all_possible_board_configurations() -> np.ndarray:
    states = np.zeros((3 ** 9, 9))

    for i, s in enumerate(states):
        mark = i
        for j in np.arange(9):
            states[i, j] = mark % 3
            mark //= 3

    states = np.where(states == 0, "-", np.where(states == 1, "x", "o"))

    return states


def _filter_valid_state(state: np.ndarray) -> bool:
    state = np.reshape(state, (3, 3))

    valid_status = False
    
    empty_count, x_count, o_count = (
        (state == "-").sum(),
        (state == "x").sum(),
        (state == "o").sum(),
    )

    if empty_count == 9:
        valid_status = True

    if x_count == o_count or x_count == o_count + 1:
        if check_player_is_winner(state, "o"):
            if check_player_is_winner(state, "x"):
                valid_status  = False

            if x_count == o_count:
                valid_status = True
        
        if check_player_is_winner(state, "x"):
            if x_count != o_count + 1:
                valid_status = False

        if not check_player_is_winner(state, "o"):
            valid_status = True

    return valid_status


def _all_valid_board_configurations() -> np.ndarray:
    all_boards = _all_possible_board_configurations()
    return np.array(list(filter(_filter_valid_state, all_boards)))


def _initial_probabilities_of_winning_from_state(mark: str) -> Dict[np.ndarray, float]:
    valid_states = _all_valid_board_configurations()

    state_winning_probability = {}

    for state in valid_states:
        is_winner = check_player_is_winner(np.reshape(state, (3, 3)), mark)
        state = "".join(state)

        if is_winner:
            state_winning_probability[state] = 1.0
        else:
            state_winning_probability[state] = 0.5
        
    return state_winning_probability
