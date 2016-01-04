from utils import *
from search import *


def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))


def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.legal_moves())


def alphabeta_player(game, state):
    return alphabeta_search(state, game)
