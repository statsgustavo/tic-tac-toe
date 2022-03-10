import os
from typing import Any, Callable, Tuple

import numpy as np
import toolz as tz

from tic_tac_toe import agent, cli_tools, errors, game


@tz.curry
def _human_interaction(game_board: np.ndarray, player_mark: str) -> np.ndarray:
    cli_tools.board_representation(game_board)
    while True:
        try:
            row, column = cli_tools.prompt_player_to_make_a_move(player_mark)
            game_board = game.update_board(game_board, row, column, player_mark)
        except (errors.MarkedPositionError, errors.BadCliUserInputError) as e:
            cli_tools.board_representation(game_board)
            print(f"[Invalid input] {e.message}")
            continue
        else:
            break

    return game_board

@tz.curry
def _bot_interaction(
    bot_instance: agent.Agent, game_board: np.ndarray, player_mark: str
) -> np.ndarray:
    row, column = bot_instance.play(game_board)
    game_board = game.update_board(game_board, row, column, player_mark)
    return game_board


def _start_session(session_type: str) -> Tuple[Any]:
    game_board = game.create_board()

    if session_type == "human_vs_human":
        p1, p2 = (
            _human_interaction(player_mark="x"), _human_interaction(player_mark="o")
        )
    
    elif session_type == "bot_vs_bot": 
        bot_1, bot_2 = agent.Agent(game_board), agent.Agent(game_board)
        p1, p2 = (
            _bot_interaction(bot_1, player_mark="x"),
            _bot_interaction(bot_2, player_mark="o")
        )
    else:
        bot = agent.Agent(game_board)

        coin_flip = np.random.choice([0, 1], 1, p=[0.5, 0.5])

        if coin_flip == 0:
            p1, p2 = (
                _human_interaction(player_mark="x"), 
                _bot_interaction(bot, player_mark="o")
            )
        else:
            p1, p2 = (
                _bot_interaction(bot, player_mark="x"), 
                _human_interaction(player_mark="o")
            )

    return game_board, p1, p2


def run_session(session_type: str) -> None:
    current_round = 0
    game_board, p1, p2 = _start_session(session_type)

    while True:
        current_round += 1
        if current_round % 2 == 0:
            player_mark = "o"
            p2(game_board=game_board)
        else:
            player_mark = "x"
            p1(game_board=game_board)
        
        cli_tools.board_representation(game_board)

        if game.check_player_is_winner(game_board, player_mark):
            cli_tools.winning_message(player_mark)
            break
        elif game.check_draw(game_board):
            cli_tools.draw_message()
            break
