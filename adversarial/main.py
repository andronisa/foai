import random
import matplotlib.pyplot as plt
import numpy as np


class MinMaxClass:
    def __init__(self, players=list()):
        self.iterations = {
            'mm': 0,
            'ab': 0
        }

    def TicTacToe(self, X, O, width=3):
        """Play a tic-tac-toe game between the two given functions. After each
        turn, yield the new board.
        Each function should get a tic-tac-toe board and a char - 'X' or 'O',
        that represents the current turn, and return the number of
        square where it wants to put a sign.
        width is the board's width and length - it's 3 as default.

        X, O -- functions
        width -- natural number
        """

        board = (set(), set(), width)

        turn = 'X'
        while self.result(board) is False:
            if turn == 'X':
                board[0].add(X(board, turn))
            else:
                board[1].add(O(board, turn))
            yield board
            turn = list({'X', 'O'} - set([turn]))[0]

    def display_tic_tac_toe(self, X, O, width=3):
        """Play a tic-tac-toe game (see TicTacToe's docstring for explanation) and
        display the new board to the user when a player plays, and the result of
        the game after its end.

        X, O - functions
        width - natural number"""
        for board in self.TicTacToe(X, O, width):
            # os.system('cls' if os.name == 'nt' else 'clear')  # clearscreen
            print("")
            print("")
            print self.str_board(board)
        winner = self.result(board)
        if winner in {'X', 'O'}:
            print winner + ' won!'
        elif winner == None:
            print 'Tie!'
        else:
            raise ValueError("The game didn't end")
        return winner, self.iterations['mm'], self.iterations['ab']

    def result(self, board):
        """Return 'X' if X won in the given board, 'O' if O won, None if the game
        ended with a tie, False if the game didn't end yet, and raise an exception
        if it looks like X and O won both (the board cannot be reached using a
        legal game)."""

        x_squares, o_squares, width = board
        rows = [{width * row + col + 1 for col in range(width)} for row in range(width)]
        cols = [{width * row + col + 1 for row in range(width)} for col in range(width)]
        diagonals = [{width * i + i + 1 for i in range(width)},
                     {width * i + width - i for i in range(width)}]

        lines = rows + cols + diagonals

        x_won = any(line.issubset(x_squares) for line in lines)
        o_won = any(line.issubset(o_squares) for line in lines)

        if x_won:
            if o_won:
                raise ValueError("Illegal board")
            return 'X'
        if o_won:
            return 'O'
        if x_squares | o_squares == set(range(1, width ** 2 + 1)):
            # Nobody won, but the board is full
            return None  # Tie

        return False

    def str_board(self, board):
        """Return the board in a string representation, to print it."""
        return_str = ''
        x_squares, o_squares, width = board
        for row in range(width):
            for col in range(width):
                square = width * row + col + 1
                return_str += 'X' if square in x_squares else 'O' if square in \
                                                                     o_squares else ' '
                if col != width - 1: return_str += ' | '
            if row != width - 1: return_str += '\n' + '--+-' * (width - 1) + '-\n'
        return return_str

    def human_player(self, board, turn):
        """Display the board to the user and ask him where does he want to put a
        sign. Return the square."""
        x_squares, o_squares, width = board
        print("")
        print("")
        print self.str_board(board)

        while True:
            try:
                square = int(
                        raw_input('Where do you want to add ' + turn + '? '))
                assert 0 < square <= width ** 2 and \
                       square not in x_squares | o_squares
                return square  # this will happen if there were no exceptions
            except:
                print ('You should write an integer between 1 and ' + str(width ** 2) +
                       ', that represents a blank square.')

    def random_player(self, board, player):
        """Return a square where it's worthwhile to play according to the minimax
        algorithm."""
        x_squares, o_squares, width = board

        available_squares = list(set(range(1, width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        return random.choice(available_squares)

    def minimax_player(self, board, player):
        """Return a square where it's worthwhile to play according to the minimax
        algorithm."""
        print("Total Iterations of minimax : " + str(self.iterations['mm']) + " - " + player)
        return self.minimax_best_square(board, player)[0]

    def minimax_score_board(self, board, turn):
        """Return 1, 0 or -1 according to the minimax algorithm -- 1 if the player
        that has the given turn has a winning strategy, 0 if he doesn't have a
        winning strategy but he has a tie strategy, and -1 if he will lose anyway
        (assuming his opponent is playing a perfect game)."""

        if self.result(board) == turn:
            return 1
        if self.result(board) is 'Tie':
            return 0
        if self.result(board) is not False:
            return -1
        return self.minimax_best_square(board, turn)[1]

    def minimax_best_square(self, board, player):
        """Choose a square where it's worthwhile to play in the given board and
        turn, and return a tuple of the square's number and it's score according
        to the minimax algorithm."""
        x_squares, o_squares, width = board
        max_score = -2

        opponent = list({'X', 'O'} - set([player]))[0]
        available_squares = list(set(range(1, width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        for square in available_squares:
            if len(available_squares) == 9:
                return square, 5
            self.iterations['mm'] += 1

            # Iterate over the blank squares, to get the best square to play
            new_board = (x_squares | set([square] if player == 'X' else []),) + \
                        (o_squares | set([square] if player == 'O' else []), width)
            score = -self.minimax_score_board(new_board, opponent)

            if score == 1:
                return square, 1

            if score > max_score:
                max_score, max_square = score, square
        return max_square, max_score

    def alpha_beta_player(self, board, player, alpha=-2, beta=2):
        """Return a square where it's worthwhile to play according to the minimax
        algorithm."""

        print("Total Iterations of minimax : " + str(self.iterations['ab']) + " - " + player)
        return self.alpha_beta_best_square(board, player, alpha, beta)[0]

    def alpha_beta_score_board(self, board, player, alpha, beta):
        """Return 1, 0 or -1 according to the minimax algorithm -- 1 if the player
        that has the given turn has a winning strategy, 0 if he doesn't have a
        winning strategy but he has a tie strategy, and -1 if he will lose anyway
        (assuming his opponent is playing a perfect game)."""

        if self.result(board) == player:
            return 1
        if self.result(board) is None:
            return 0
        if self.result(board) is not False:
            return -1
        return self.alpha_beta_best_square(board, player, alpha, beta)[1]

    def alpha_beta_best_square(self, board, player, alpha, beta):
        """Choose a square where it's worthwhile to play in the given board and
        turn, and return a tuple of the square's number and it's score according
        to the minimax algorithm."""
        x_squares, o_squares, width = board

        opponent = list({'X', 'O'} - set([player]))[0]
        available_squares = list(set(range(1, width ** 2 + 1)) - (x_squares | o_squares))
        random.shuffle(available_squares)

        for square in available_squares:
            self.iterations['ab'] += 1

            # Iterate over the blank squares, to get the best square to play
            new_board = (x_squares | set([square] if player == 'X' else []),) + \
                        (o_squares | set([square] if player == 'O' else []), width)
            score = -self.alpha_beta_score_board(new_board, opponent, alpha, beta)

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
    result = {
        'mm_iters': [],
        'ab_iters': [],
        'mm_wins': 0,
        'ab_wins': 0,
        'ties': 0,
    }

    for i in range(100):
        solver = MinMaxClass(['mm', 'ab'])
        minmax_against_alphabeta = solver.display_tic_tac_toe(X=solver.minimax_player, O=solver.alpha_beta_player,
                                                              width=3)
        if minmax_against_alphabeta[0] == 'X':
            result['mm_wins'] += 1
        elif minmax_against_alphabeta[0] == 'O':
            result['ab_wins'] += 1
        else:
            result['ties'] += 1
        result['mm_iters'].append(minmax_against_alphabeta[1])
        result['ab_iters'].append(minmax_against_alphabeta[2])
    return result


def ab_vs_mm():
    result = {
        'mm_iters': [],
        'ab_iters': [],
        'mm_wins': 0,
        'ab_wins': 0,
        'ties': 0,
    }

    for i in range(100):
        solver = MinMaxClass(['mm', 'ab'])
        minmax_against_alphabeta = solver.display_tic_tac_toe(X=solver.alpha_beta_player, O=solver.minimax_player,
                                                              width=3)
        if minmax_against_alphabeta[0] == 'O':
            result['mm_wins'] += 1
        elif minmax_against_alphabeta[0] == 'X':
            result['ab_wins'] += 1
        else:
            result['ties'] += 1
        result['mm_iters'].append(minmax_against_alphabeta[1])
        result['ab_iters'].append(minmax_against_alphabeta[2])
    return result


if __name__ == "__main__":
    solver = MinMaxClass(['mm', 'ab'])
    # solver.display_tic_tac_toe(X=solver.human_player, O=solver.alpha_beta_player, width=3)
    # result = solver.display_tic_tac_toe(X=solver.minimax_player, O=solver.alpha_beta_player, width=3)
    result = mm_vs_ab()
    OX = [
        'MinMax',
        'Alpha Beta',
        'Ties'
    ]

    mm = result['mm_wins']
    ab = result['ab_wins']
    ties = result['ties']

    OY = [mm, ab, ties]

    fig = plt.figure()

    width = .20
    ind = np.arange(len(OY))
    barlist = plt.bar(ind, OY, align='center')
    plt.xticks(ind + width / 2, OX)

    barlist[0].set_color('r')
    barlist[1].set_color('b')
    barlist[2].set_color('g')
    plt.legend((barlist[0], barlist[1], barlist[2]),
               ('MinMax Wins: ' + str(mm), 'AlphaBeta Wins: ' + str(ab), 'Ties: ' + str(ties)))

    plt.xlabel('Winner')
    plt.ylabel('Wins Count')
    plt.title('Tic Tac Toe - MinMax vs Alpha-Beta')
    plt.show()
    # raw_input()
