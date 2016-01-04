from tic_tac_toe import TicTacToe
from players import *


def play_game(game, *players):
    "Play an n-person, move-alternating game."
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.make_move(move, state)
            if game.terminal_test(state):
                return game.utility(state, players[0])


if __name__ == "__main__":
    game = TicTacToe()
    play_game(game, random_player, [alphabeta_player])
