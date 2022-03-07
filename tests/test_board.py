from unittest.loader import VALID_MODULE_NAME

import hypothesis as hp
import pytest
from hypothesis import strategies as st
from tic_tac_toe import board, errors


@pytest.fixture(scope="session")
def game_board():
    return board.create_board()


def test_board_shape(game_board):
    assert game_board.shape == (3, 3)


def test_board_filled_with_one_characters(game_board):
    assert (game_board == "-").all()


@hp.given(row=st.integers(0, 2), column=st.integers(0, 2), mark=st.integers(0, 1))
def test_board_update_on_already_marked_positions(row, column, mark):
    game_board = board.create_board()

    player_mark = "x" if mark == 1 else "o"
    updated_board = board.update_board(game_board, row, column, player_mark)

    with pytest.raises(errors.MarkedPositionError):
        board.update_board(updated_board, row, column, player_mark)


@hp.given(row=st.integers(0, 2), column=st.integers(0, 2), mark=st.integers(0, 1))
def test_board_update(row, column, mark):
    game_board = board.create_board()

    _mark = "x" if mark == 0 else "o"
    
    updated_board = board.update_board(game_board, row, column, _mark)
    print(updated_board)
    assert updated_board[row, column] == _mark


# @hp.given(row=st.integers(0, 2), column=st.integers(0, 2), mark=st.characters())
# def test_board_update_with_invalid_values(row, column, mark):    
#     game_board = board.create_board()

#     if mark.lower() in  ["x", "o"]:
#         pass
#     else:
#         with pytest.raises(errors.BadMarkError):
#             board.update_board(game_board, row, column, mark)


@hp.given(row=st.integers(0, 2), mark=st.integers(0, 1))
def test_row_win_verification(row, mark):
    game_board = board.create_board()

    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_columns = game_board.shape[1]
    while i < num_columns:
        game_board = board.update_board(game_board, row, i, player_mark)
        i += 1
        
    assert board.check_player_is_winner(game_board, player_mark)


@hp.given(column=st.integers(0, 2), mark=st.integers(0, 1)) 
def test_column_win_verification(column, mark):
    game_board = board.create_board()

    player_mark = "x" if mark == 0 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = board.update_board(game_board, i, column, player_mark)
        i += 1
        
    assert board.check_player_is_winner(game_board, player_mark)


@hp.given(mark=st.integers(0, 1)) 
def test_main_diagonal_win_verification(mark):
    game_board = board.create_board()

    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = board.update_board(game_board, i, i, player_mark)
        i += 1
        
    assert board.check_player_is_winner(game_board, player_mark)


@hp.given(mark=st.integers(0, 1)) 
def test_secondary_diagonal_win_verification(game_board, mark):
    game_board = board.create_board()
    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = board.update_board(game_board, i, num_rows - (i + 1), player_mark)
        i += 1
        
    assert board.check_player_is_winner(game_board, player_mark)


