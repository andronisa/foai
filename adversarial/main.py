import random
import matplotlib.pyplot as plt
import numpy as np


class MinMaxClass:
    def __init__(self, players=list()):
        self.iterations = {
            'mm': 0,
            'ab': 0
        }

    def Tic_Tac_Toe(self, X, O, game_width=3):
        tile_board = (set(), set(), game_width)

        player = 'X'
        while self.calculate(tile_board) is False:
            if player == 'X':
                tile_board[0].add(X(tile_board, player))
            else:
                tile_board[1].add(O(tile_board, player))
            yield tile_board
            player = list({'X', 'O'} - set([player]))[0]

    def display_tic_tac_toe(self, X, O, game_width=3):
        for tile_board in self.Tic_Tac_Toe(X, O, game_width):
            # os.system('cls' if os.name == 'nt' else 'clear')  # clearscreen
            print("")
            print("")
            print self.print_board(tile_board)
        winner = self.calculate(tile_board)
        if winner in {'X', 'O'}:
            print winner + ' won!'
        elif winner == None:
            print 'Tie!'
        else:
            raise ValueError("The game didn't end")
        return winner, self.iterations['mm'], self.iterations['ab']

    def calculate(self, tile_board):
        x_squares, o_squares, game_width = tile_board
        rrrs = [{game_width * rrr + col + 1 for col in range(game_width)} for rrr in range(game_width)]
        cols = [{game_width * rrr + col + 1 for rrr in range(game_width)} for col in range(game_width)]
        diagonals = [{game_width * i + i + 1 for i in range(game_width)},
                     {game_width * i + game_width - i for i in range(game_width)}]

        lines = rrrs + cols + diagonals

        x_won = any(line.issubset(x_squares) for line in lines)
        o_won = any(line.issubset(o_squares) for line in lines)

        if x_won:
            if o_won:
                raise ValueError("Illegal tile_board")
            return 'X'
        if o_won:
            return 'O'
        if x_squares | o_squares == set(range(1, game_width ** 2 + 1)):
            # Nobody won, but the tile_board is full
            return None  # Tie

        return False

    def print_board(self, tile_board):
        return_str = ''
        x_squares, o_squares, game_width = tile_board
        for rrr in range(game_width):
            for col in range(game_width):
                square = game_width * rrr + col + 1
                return_str += 'X' if square in x_squares else 'O' if square in \
                                                                     o_squares else ' '
                if col != game_width - 1: return_str += ' | '
            if rrr != game_width - 1: return_str += '\n' + '--+-' * (game_width - 1) + '-\n'
        return return_str

    def human_player(self, tile_board, player):

        x_squares, o_squares, game_width = tile_board
        print("")
        print("")
        print self.print_board(tile_board)

        while True:
            try:
                square = int(
                        raw_input('Where do you want to add ' + player + '? '))
                assert 0 < square <= game_width ** 2 and \
                       square not in x_squares | o_squares
                return square  # this will happen if there were no exceptions
            except:
                print ('You should write an integer between 1 and ' + str(game_width ** 2) +
                       ', that represents a blank square.')

    def random_player(self, tile_board, player):
        x_squares, o_squares, game_width = tile_board

        available_squares = list(set(range(1, game_width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        return random.choice(available_squares)

    def minimax_player(self, tile_board, player):

        print("Total Iterations of minimax : " + str(self.iterations['mm']) + " - " + player)
        return self.minimax_best_square(tile_board, player)[0]

    def minimax_score_tile_board(self, tile_board, player):
        if self.calculate(tile_board) == player:
            return 1
        if self.calculate(tile_board) is 'Tie':
            return 0
        if self.calculate(tile_board) is not False:
            return -1
        return self.minimax_best_square(tile_board, player)[1]

    def minimax_best_square(self, tile_board, player):
        x_squares, o_squares, game_width = tile_board
        max_score = -2

        opponent = list({'X', 'O'} - set([player]))[0]
        available_squares = list(set(range(1, game_width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        for square in available_squares:
            if len(available_squares) == 9:
                return square, 5
            self.iterations['mm'] += 1

            # Iterate over the blank squares, to get the best square to play
            new_tile_board = (x_squares | set([square] if player == 'X' else []),) + \
                             (o_squares | set([square] if player == 'O' else []), game_width)
            score = -self.minimax_score_tile_board(new_tile_board, opponent)

            if score == 1:
                return square, 1

            if score > max_score:
                max_score, max_square = score, square
        return max_square, max_score

    def alpha_beta_player(self, tile_board, player, alpha=-2, beta=2):
        print("Total Iterations of minimax : " + str(self.iterations['ab']) + " - " + player)
        return self.alpha_beta_best_square(tile_board, player, alpha, beta)[0]

    def alpha_beta_score_tile_board(self, tile_board, player, alpha, beta):

        if self.calculate(tile_board) == player:
            return 1
        if self.calculate(tile_board) is None:
            return 0
        if self.calculate(tile_board) is not False:
            return -1
        return self.alpha_beta_best_square(tile_board, player, alpha, beta)[1]

    def alpha_beta_best_square(self, tile_board, player, alpha, beta):
        """Choose a square where it's worthwhile to play in the given tile_board and
        turn, and return a tuple of the square's number and it's score according
        to the minimax algorithm."""
        x_squares, o_squares, game_width = tile_board

        opponent = list({'X', 'O'} - set([player]))[0]
        available_squares = list(set(range(1, game_width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        for square in available_squares:
            self.iterations['ab'] += 1

            # Iterate over the blank squares, to get the best square to play
            new_tile_board = (x_squares | set([square] if player == 'X' else []),) + \
                             (o_squares | set([square] if player == 'O' else []), game_width)
            score = -self.alpha_beta_score_tile_board(new_tile_board, opponent, alpha, beta)

            if player == 'O':
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return square, beta
            else:
                if score < beta:
                    beta = score
                if beta <= alpha:
                    return square, alpha

        if player == 'O':
            return square, alpha
        else:
            return square, beta


def mm_vs_ab():
    calculate = {
        'mm_iters': [],
        'ab_iters': [],
        'mm_wins': 0,
        'ab_wins': 0,
        'ties': 0,
    }

    for i in range(100):
        solver = MinMaxClass(['mm', 'ab'])
        minmax_against_alphabeta = solver.display_tic_tac_toe(X=solver.minimax_player, O=solver.alpha_beta_player,
                                                              game_width=3)
        if minmax_against_alphabeta[0] == 'X':
            calculate['mm_wins'] += 1
        elif minmax_against_alphabeta[0] == 'O':
            calculate['ab_wins'] += 1
        else:
            calculate['ties'] += 1
        calculate['mm_iters'].append(minmax_against_alphabeta[1])
        calculate['ab_iters'].append(minmax_against_alphabeta[2])
    return calculate


def ab_vs_mm():
    calculate = {
        'mm_iters': [],
        'ab_iters': [],
        'mm_wins': 0,
        'ab_wins': 0,
        'ties': 0,
    }

    for i in range(100):
        solver = MinMaxClass(['mm', 'ab'])
        minmax_against_alphabeta = solver.display_tic_tac_toe(X=solver.alpha_beta_player, O=solver.minimax_player,
                                                              game_width=3)
        if minmax_against_alphabeta[0] == 'O':
            calculate['mm_wins'] += 1
        elif minmax_against_alphabeta[0] == 'X':
            calculate['ab_wins'] += 1
        else:
            calculate['ties'] += 1
        calculate['mm_iters'].append(minmax_against_alphabeta[1])
        calculate['ab_iters'].append(minmax_against_alphabeta[2])
    return calculate


def plot_wins(calculate, title):
    OX = [
        'MinMax',
        'Alpha Beta',
        'Tie'
    ]

    mm = calculate['mm_wins']
    ab = calculate['ab_wins']
    ties = calculate['ties']

    OY = [mm, ab, ties]

    fig = plt.figure()

    game_width = .20
    ind = np.arange(len(OY))
    barlist = plt.bar(ind, OY, align='center')
    plt.xticks(ind + game_width / 2, OX)

    barlist[0].set_color('r')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    plt.legend((barlist[0], barlist[1], barlist[2]),
               ('MinMax Wins: ' + str(mm), 'AlphaBeta Wins: ' + str(ab), 'Ties: ' + str(ties)))

    plt.xlabel('Result')
    plt.ylabel('Wins Count')
    plt.title(title)
    plt.show()


def plot_lines(calculate, limit, title):
    mm = calculate['mm_iters']
    ab = calculate['ab_iters']
    mm_average = sum(mm) / len(mm)
    ab_average = sum(ab) / len(ab)

    lines = plt.plot(mm, 'xr-', ab, 'xb-', game_width=4)

    plt.legend((lines[0], lines[1]),
               ('MinMax average iterations: ' + str(mm_average), 'AlphaBeta average iterations: ' + str(ab_average)),
               loc=1)

    plt.xlabel('Games')
    plt.ylabel('Number of Iterations')
    plt.title(title)
    x1, x2, y1, y2 = plt.axis()

    plt.axis((x1, x2, 0, limit))
    plt.show()


if __name__ == "__main__":
    solver = MinMaxClass(['mm', 'ab'])
    # solver.display_tic_tac_toe(X=solver.human_player, O=solver.alpha_beta_player, game_width=3)
    # calculate = solver.display_tic_tac_toe(X=solver.minimax_player, O=solver.alpha_beta_player, game_width=3)
    calculate = mm_vs_ab()
    plot_wins(calculate, 'Tic Tac Toe - MinMax vs AlphaBeta')
    plot_lines(calculate, 1800, 'Tic Tac Toe - AlphaBeta vs MinMax - Execution iterations')

    calculate = ab_vs_mm()
    plot_wins(calculate, 'Tic Tac Toe - AlphaBeta vs MinMax')
    plot_lines(calculate, 1800, 'Tic Tac Toe - AlphaBeta vs MinMax - Execution iterations')

    # raw_input()
