import numpy as np

from tic_tac_toe import game


class Agent:

    def __init__(self, game_board, epsilon=0.05, number_of_games_won=0):
        self._game_board = game_board
        self._epsilon = epsilon
        self._number_of_games_won = number_of_games_won

    def _translate_board_to_string(self):
        return "".join(self._game_board.ravel())

    def _get_available_positions_on_the_board(self):
        return np.argwhere(self._game_board == "-")

    def _update_board_knowledge(self, game_board):
        self._game_board = game_board

    def play(self, game_board):
        self._update_board_knowledge(game_board)

        possible_moves = self._get_available_positions_on_the_board()
        move_idx = np.random.choice(possible_moves.shape[0], 1)[0]
        row, col = possible_moves[move_idx]

        return row, col
