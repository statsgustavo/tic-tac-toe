import os
from re import X
from typing import Tuple

import numpy as np
import toolz as tz

from tic_tac_toe import errors


def _color_text(text, color, bold=False):
    make_bold = "\u001b[1m"
    reset_color = "\u001b[0m"
    colors = {
        "green": "\u001b[32m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
    }

    text = f"{colors.get(color, reset_color)}{text}{reset_color}"

    if bold:
        text = f"{make_bold}{text}"

    return text


def _decode_row_and_column(positions: Tuple[str]) -> Tuple[int]:
    row, column = positions

    rows = {"1": 0, "2": 1, "3": 2}
    columns = {"a": 0, "b": 1, "c": 2}

    if (row not in rows.keys()) or (column not in columns.keys()):
        raise errors.BadCliUserInputError(positions)

    return rows[row], columns[column]


def _parse_input_string(input_str: str) -> Tuple[str]:
    input_tuple = input_str.split(",")

    if len(input_tuple) != 2:
        raise errors.BadCliUserInputError(
            input_tuple, "Row and column positions must be separated by comma."
        )

    return tuple(
        map(
            lambda s: s.strip(), input_tuple
        )
    )


def prompt_player_to_make_a_move(player_id: str) -> Tuple[int]:
    user_input =  input(
        f"[{player_id}'s turn] Type the row and column positions on the board " + 
        "you want to lock, separarared by comma:\n>> "
    )

    return tz.pipe(user_input, _parse_input_string, _decode_row_and_column)


def board_representation(board: np.array) -> None:
    os.system("clear")

    board = np.where(
        board == "-", "-",
        np.where(
            board == "x", 
            _color_text("X", "green", True),
            _color_text("O", "magenta", True)
        )
    )


    left_padding = "\t\t\t"
    top_bottom_padding = "\n\n\n"
    header =           f"{left_padding}   a     b     c  \n"
    top_bottom_row =   f"{left_padding}      |     |     \n"
    intermediary_row = f"{left_padding} _____|_____|_____\n"
    row1 = f"{left_padding}1  {board[0, 0]}  |  {board[0, 1]}  |  {board[0, 2]}  \n"
    row2 = f"{left_padding}2  {board[1, 0]}  |  {board[1, 1]}  |  {board[1, 2]}  \n"
    row3 = f"{left_padding}3  {board[2, 0]}  |  {board[2, 1]}  |  {board[2, 2]}  \n"


    board_repr = (
        top_bottom_padding
        + header 
        + top_bottom_row 
        + row1 
        + intermediary_row 
        + top_bottom_row 
        + row2 
        + intermediary_row
        + top_bottom_row  
        + row3 
        + top_bottom_row
        + top_bottom_padding
    )
    print(board_repr)


def winning_message(player_id: str) -> str:
    x_wins_message = """
    ###      ###        ###           ###  ###  ####      ###  ##########    ####
     ###    ###         ###           ###  ###  #####     ###  ####          ####
      ###  ###          ###           ###  ###  ### ###   ###  ####          ####
        ###             ###    ###    ###  ###  ###  ###  ###  ##########    ####
      ###  ###          ###  ### ###  ###  ###  ###   ### ###        ####    ####
     ###    ###         ### ###   ### ###  ###  ###     #####        ####        
    ###      ###          ###       ###    ###  ###      ####  ##########    ####
    """


    o_wins_message = """
       ######           ###           ###  ###  ####      ###  ##########    ####
     ###    ###         ###           ###  ###  #####     ###  ####          ####
    ###      ###        ###           ###  ###  ### ###   ###  ####          ####
    ###      ###        ###    ###    ###  ###  ###  ###  ###  ##########    ####
    ###      ###        ###  ### ###  ###  ###  ###   ### ###        ####    ####
     ###    ###         ### ###   ### ###  ###  ###     #####        ####    
       ######             ###       ###    ###  ###      ####  ##########    ####
    """

    print(
        _color_text(x_wins_message, "green")
        if player_id == "x" 
        else _color_text(o_wins_message, "magenta")
    )


def draw_message() -> None:
    message = """
    #########      ########           ###        ###           ###                
    ###     ###    ###    ###        #####       ###           ###                
    ###      ###   ###    ###       ### ###      ###           ###                     
    ###       ###  ### ###         ###   ###     ###    ###    ###             
    ###      ###   ###   ###      ### ### ###    ###  ### ###  ###                           
    ###     ###    ###    ###    ###       ###   ### ###   ### ###   ###  ###  ###          
    #########      ###     ###  ###         ###    ###       ###     ###  ###  ###           
    """

    print(_color_text(message, "cyan"))
