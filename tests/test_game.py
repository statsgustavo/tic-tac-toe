
import hypothesis as hp
import numpy as np
import pytest
from hypothesis import strategies as st
from tic_tac_toe import errors, game


@pytest.fixture(scope="session")
def game_board():
    return game.create_board()


def test_board_shape(game_board):
    assert game_board.shape == (3, 3)


def test_board_filled_with_one_characters(game_board):
    assert (game_board == "-").all()


@hp.given(row=st.integers(0, 2), column=st.integers(0, 2), mark=st.integers(0, 1))
def test_board_update_on_already_marked_positions(row, column, mark):
    game_board = game.create_board()

    player_mark = "x" if mark == 1 else "o"
    updated_board = game.update_board(game_board, row, column, player_mark)

    with pytest.raises(errors.MarkedPositionError):
        game.update_board(updated_board, row, column, player_mark)


@hp.given(row=st.integers(0, 2), column=st.integers(0, 2), mark=st.integers(0, 1))
def test_board_update(row, column, mark):
    game_board = game.create_board()

    _mark = "x" if mark == 0 else "o"
    
    updated_board = game.update_board(game_board, row, column, _mark)
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
    game_board = game.create_board()

    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_columns = game_board.shape[1]
    while i < num_columns:
        game_board = game.update_board(game_board, row, i, player_mark)
        i += 1
        
    assert game.check_player_is_winner(game_board, player_mark)


@hp.given(column=st.integers(0, 2), mark=st.integers(0, 1)) 
def test_column_win_verification(column, mark):
    game_board = game.create_board()

    player_mark = "x" if mark == 0 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = game.update_board(game_board, i, column, player_mark)
        i += 1
        
    assert game.check_player_is_winner(game_board, player_mark)


@hp.given(mark=st.integers(0, 1)) 
def test_main_diagonal_win_verification(mark):
    game_board = game.create_board()

    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = game.update_board(game_board, i, i, player_mark)
        i += 1
        
    assert game.check_player_is_winner(game_board, player_mark)


@hp.given(mark=st.integers(0, 1)) 
def test_secondary_diagonal_win_verification(game_board, mark):
    game_board = game.create_board()
    player_mark = "x" if mark == 1 else "o"

    i = 0
    num_rows = game_board.shape[0]
    while i < num_rows:
        game_board = game.update_board(game_board, i, num_rows - (i + 1), player_mark)
        i += 1
        
    assert game.check_player_is_winner(game_board, player_mark)



def test_valid_state_filter():
    state1 = np.array([["o", "x", "x"],["-", "o", "x"],["-", "x", "o"]])
    state2 = np.array([["x", "o", "o"],["-", "x", "o"],["-", "o", "x"]])
    state3 = np.array([["x", "o", "o"],["-", "x", "-"],["-", "-", "x"]])
    state4 = np.array([["x", "o", "o"],["o", "x", "x"],["x", "x", "o"]])
    state5 = np.array([["o", "x", "x"],["x", "x", "-"],["o", "o", "o"]])
    state6 = np.array([['-', '-', 'x'],['o', 'x', 'o'],['x', '-', '-']])

    assert game._filter_valid_state(state1) == False
    assert game._filter_valid_state(state2) == False
    assert game._filter_valid_state(state3) == True
    assert game._filter_valid_state(state4) == True
    assert game._filter_valid_state(state5) == True
    assert game._filter_valid_state(state6) == True


