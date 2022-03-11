import numpy as np
import pytest
from tic_tac_toe import agent, game


@pytest.fixture(scope="module")
def board():
    return np.array([["-", "x", "o"], ["-", "x", "o"], ["-", "-", "x"]])


def test_board_to_string_translation(board):
    assert agent.Agent(board)._translate_board_to_string() == "-xo-xo--x"


def test_find_available_positions_on_the_board(board):
    assert (
        agent.Agent(board)._get_available_positions_on_the_board()
        == [
            [0, 0],
            [1, 0],
            [2, 0],
            [2, 1],
        ]
    ).all()


def test_update_board_knowledge(board):
    assert (
        agent.Agent(board)
        ._update_board_knowledge(
            np.array([["x", "x", "o"], ["-", "x", "o"], ["-", "-", "x"]])
        )
        ._translate_board_to_string()
    ) == "xxo-xo--x"
