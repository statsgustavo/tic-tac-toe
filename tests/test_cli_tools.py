import pytest
from tic_tac_toe import cli_tools, errors


def test_user_input_parser():
    input_ = "1, a"
    assert cli_tools._parse_input_string(input_) == ("1", "a")


def test_user_input_with_different_separator():
    input_ = "1. a"
    with pytest.raises(errors.BadCliUserInputError): 
        cli_tools._parse_input_string(input_) == ("1", "a")
