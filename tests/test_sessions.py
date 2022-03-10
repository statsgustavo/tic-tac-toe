import contextlib
import io
import sys

import pytest
from tic_tac_toe import game, sessions


@contextlib.contextmanager
def output():
    incoming_out, incoming_err = io.StringIO(), io.StringIO()
    current_out, current_err = sys.stdout, sys.stderr

    try:
        sys.stdout, sys.stderr = incoming_out, incoming_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = current_out, current_err


@pytest.fixture(scope="session")
def x_mark():
    return "\u001b[1m\u001b[32mX\u001b[0m"


@pytest.fixture(scope="session")
def o_mark():
    return "\u001b[1m\u001b[35mO\u001b[0m"

@pytest.fixture(scope="session")
def board():
    return game.create_board()


def test_human_interaction_for_starting_player(capsys, board):
    sys.stdin = io.StringIO("1,a")
    sessions._human_interaction(board, "x")
    out, err = capsys.readouterr()

    expected_out = (
        "\n\n\n"
        + f"\t\t\t   a     b     c  \n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t1  -  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t2  -  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t3  -  |  -  |  -  \n"
        + f"\t\t\t      |     |     \n"
        + "\n\n\n"
        + "\n[x's turn] Type the row and column positions on the"
        + " board you want to lock, separarared by comma:\n>> "
    )
    assert err == ""
    assert out == expected_out


def test_human_interaction_for_second_player(capsys, board, x_mark, o_mark):
    sys.stdin = io.StringIO("2,b")
    sessions._human_interaction(board, "o")
    out, err = capsys.readouterr()

    expected_out = (
        "\n\n\n"
        + f"\t\t\t   a     b     c  \n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t1  {x_mark}  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t2  -  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t3  -  |  -  |  -  \n"
        + f"\t\t\t      |     |     \n"
        + "\n\n\n"
        + "\n[o's turn] Type the row and column positions on the"
        + " board you want to lock, separarared by comma:\n>> "
    )
    assert err == ""
    assert out == expected_out


def test_human_interaction_invalid_input(capsys, monkeypatch, board, x_mark, o_mark):
    interactions = iter(["2,g", "2,a"])
    monkeypatch.setattr("builtins.input", lambda _: next(interactions))

    sessions._human_interaction(board, "x")
    
    out, err = capsys.readouterr()

    _board = (
        "\n\n\n"
        + f"\t\t\t   a     b     c  \n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t1  {x_mark}  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t2  -  |  {o_mark}  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t3  -  |  -  |  -  \n"
        + f"\t\t\t      |     |     \n"
        + "\n\n\n"
    )

    expected_out = (
        _board
        + "\n"
        + _board
        + "\n"
        + "[Invalid input] Values for rows are ('1', '2' or '3') and "
        + "for columns are ('a', 'b' or 'c').\n"
    )

    print(out)
    assert err == ""
    assert out == expected_out



def test_human_interaction_input_on_unavailable_position(
    capsys, monkeypatch, board, x_mark, o_mark
):
    interactions = iter(["2,b", "2,c"])
    monkeypatch.setattr("builtins.input", lambda _: next(interactions))

    sessions._human_interaction(board, "o")
    
    out, err = capsys.readouterr()

    _board = (
        "\n\n\n"
        + f"\t\t\t   a     b     c  \n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t1  {x_mark}  |  -  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t2  {x_mark}  |  {o_mark}  |  -  \n"
        + f"\t\t\t _____|_____|_____\n"
        + f"\t\t\t      |     |     \n"
        + f"\t\t\t3  -  |  -  |  -  \n"
        + f"\t\t\t      |     |     \n"
        + "\n\n\n"
    )

    expected_out = (
        _board
        + "\n"
        + _board
        + "\n"
        + "[Invalid input] Position was already chosen by another player.\n"
    )
    
    assert err == ""
    assert out == expected_out
