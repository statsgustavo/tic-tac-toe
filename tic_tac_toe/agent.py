import numpy as np

from tic_tac_toe import game


class Agent:
    def __init__(self, game_board):
        self._game_board = game_board

    def _get_available_positions_on_the_board(self):
        return np.argwhere(self._game_board == "-")

    def _update_board_knowledge(self, game_board):
        self._game_board = game_board
        return self

    def play(self, game_board):
        possible_moves = self._update_board_knowledge(
            self, game_board
        )._get_available_positions_on_the_board()

        move_idx = np.random.choice(possible_moves.shape[0], 1)[0]
        row, col = possible_moves[move_idx]

        return row, col
