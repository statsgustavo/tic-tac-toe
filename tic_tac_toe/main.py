import fire
import toolz as tz

from tic_tac_toe import sessions


def play_game(mode: str = "human_vs_bot") -> None:
    """
    Tic-tac-toe game session.

    :param mode: a string indicating the type vesus mode the game will run on. Valid
    modes are "human_vs_human", "human_vs_bot" or "bot_vs_bot"
    """

    valid_modes = ["human_vs_bot", "human_vs_human", "bot_vs_bot"]
    if mode not in valid_modes or mode is None:
        mode = "human_vs_bot"

    sessions.run_session(mode)


def cli():
    """Command line tic-tac-toe game."""
    fire.Fire(play_game)

if __name__ == "__main__":
    cli()
