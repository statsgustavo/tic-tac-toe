import toolz as tz

from tic_tac_toe import board, cli_tools, errors


def request_input(game_board, player_mark):
    while True:
        try:
            row, column = cli_tools.prompt_player_to_make_a_move(player_mark)
            game_board = board.update_board(game_board, row, column, player_mark)
        except (errors.MarkedPositionError, errors.BadCliUserInputError) as e:
            cli_tools.board_representation(game_board)
            print(f"[{player_mark}'s turn] {e.message}")
            continue
        else:
            break

    return game_board


def main():
    rounds = 0
    game_board = board.create_board()
    cli_tools.board_representation(game_board)
    while True:
        rounds += 1

        if rounds % 2 == 0:
            player_mark = "o"
        else:
            player_mark = "x"

        #row, column = cli_tools.prompt_player_to_make_a_move(player_mark)
        game_board = request_input(game_board, player_mark)
        
        #game_board = board.update_board(game_board, row, column, player_mark)
        cli_tools.board_representation(game_board)

        if board.check_player_is_winner(game_board, player_mark):
            #print(f"{player_mark}'s win!")
            cli_tools.winning_message(player_mark)
            break
        elif board.check_draw(game_board):
            cli_tools.draw_message()
            break


if __name__ == "__main__":
    main()
