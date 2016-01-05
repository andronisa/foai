#!/usr/bin/env python
"""
 a python Tic Tac Toe implementation

 Sample session :

    $ ./tictactoe.py
     === Tic Tac Toe ===
     Inputs may be abbreviated by their first letter.
     Type 'quit' at any prompt to quit.
     X always goes first.

     == Playing a new game. ==
     Player X is user, random, or smart ? smart
     Player O is user, random, or smart ? random

         |   |            a | b | c
      ---+---+---        ---+---+---
         |   |            d | e | f
      ---+---+---        ---+---+---
         |   |            g | h | i

     SmartPlayer X chooses i.

         |   |            a | b | c
      ---+---+---        ---+---+---
         |   |            d | e | f
      ---+---+---        ---+---+---
         |   | X          g | h | i

     RandomPlayer O chooses g.

         |   |            a | b | c
      ---+---+---        ---+---+---
         |   |            d | e | f
      ---+---+---        ---+---+---
       O |   | X          g | h | i

     SmartPlayer X chooses a.

       X |   |            a | b | c
      ---+---+---        ---+---+---
         |   |            d | e | f
      ---+---+---        ---+---+---
       O |   | X          g | h | i

     RandomPlayer O chooses c.

       X |   | O          a | b | c
      ---+---+---        ---+---+---
         |   |            d | e | f
      ---+---+---        ---+---+---
       O |   | X          g | h | i

     SmartPlayer X chooses e.

       X |   | O          a | b | c
      ---+---+---        ---+---+---
         | X |            d | e | f
      ---+---+---        ---+---+---
       O |   | X          g | h | i

     X wins!

     == Playing a new game. ==
     Player X is user, random, or smart ? quit

     Bye.

 history :
   * Oct 2006 : created with simple syntax for an intro programming course
   * Feb 2010 : cleaned up; alphabeta search added for programming workshop

 Jim Mahoney | Marlboro College | GPL
"""

#
# Board coordinates are(row,column) points           0,0 | 0,1 | 0,2
#                                                   -----+-----+-----
#                                                    1,0 | 1,1 | 1,2
#                                                   -----+-----+-----
#                                                    2,0 | 2,1 | 2,2
#
# or letters for easier user input.                  a | b | c
#                                                   ---+---+---
#                                                    d | e | f
#                                                   ---+---+---
#                                                    g | h | i
#
# The symbols on the board are
#   'X'    first player,
#   'O'    second player, or
#   ' '    empty.
#

import sys, random

infinity = float('inf')


def letter2point(letter):
    """ Convert a letter 'a'...'i' to a point (0,0) to (2,2).
        >>> letter2point('a')
        (0, 0)
        >>> letter2point('b')
        (0, 1)
        >>> letter2point('d')
        (1, 0)
    """
    zeroToEight = ord(letter) - ord('a')
    assert (0 <= zeroToEight <= 8)
    row = int(zeroToEight / 3)  # 0, 0, 0, 1, 1, 1, 2, 2, 2
    column = zeroToEight % 3  # 0, 1, 2, 0, 1, 2, 0, 1, 2
    return (row, column)


def point2letter(point):
    """ Convert a point (0,0) to (2,2) to a letter 'a' ... 'i'.
        >>> point2letter((0,0))
        'a'
        >>> point2letter((2,2))
        'i'
    """
    (row, column) = point
    return chr(ord('a') + row * 3 + column)


def quit():
    print "\n Bye. "
    sys.exit()


def ask(question, legalResponses=()):
    """ Get and return a user entered string.
        If the first letter is 'q' (for 'quit'), quit the program.
        A list of legal responses (first letters) may be specified;
        if so, keep asking until one of those is seen. """
    while True:
        try:
            answer = raw_input(question)
        except EOFError:  # user types control-d
            quit()
        if (answer):
            firstChar = answer[0]
        else:
            firstChar = ""
        if (firstChar == 'q'):
            quit()
        elif (firstChar in legalResponses or not legalResponses):
            return answer
        else:
            print "  Oops: first letter isn't in %s; please try again." \
                  % str(legalResponses + ('q',))


class RandomPlayer(object):
    """ A computer player that makes random moves. """

    def __init__(self, symbol, verbose=True):
        """ symbol is X (first player) or O (second player) """
        self.symbol = symbol
        self.verbose = verbose

    def printMove(self, move):
        if self.verbose:
            print " %s %s chooses %s.\n" \
                  % (self.__class__.__name__, self.symbol, point2letter(move))

    def getMove(self, board):
        """ Return this player's next move as a (row,column) point. """
        move = random.choice(board.possibleMoves())
        self.printMove(move)
        return move


class InteractivePlayer(RandomPlayer):
    """ A person typing in moves from the console. """
    legalLetters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')

    # legalLetters = map(chr, range(ord('a'), ord('j')))  #  same but nerdier.

    def getMove(self, board):
        """ Return the (row,column) point taken from user's input. """
        while True:
            prompt = " %s : Where do you want to move? " % self.symbol
            move = letter2point(ask(prompt, self.legalLetters))
            if (board[move] != ' '):
                print "  Oops: that place is occupied.  Try again."
            else:
                print
                return move


class SmartPlayer(RandomPlayer):
    """ A smart computer player using alphabeta/minmax search. """
    gameStartRandomMoves = 1  # for variety on opening move(s)

    def getMove(self, board):
        nMoves = board.nMovesMade()
        # print " *debug* nmoves=%i" % nMoves
        if nMoves < self.gameStartRandomMoves:
            # print " *debug* moving randomly "
            return RandomPlayer.getMove(self, board)
        else:
            (value, history) = board.alphabeta(-infinity, infinity, [], [])
            # print " *debug* alphabeta gives value=%s, history=%s" \
            #     % (str(value), str(history))
            move = history[nMoves]
            self.printMove(move)
            return move


class Board(object):
    """ The game implementation: board, moves, and search engine.
        >>> board = Board()
        >>> board[(1,1)]         # board access with a point ...
        ' '
        >>> board[1,1]           # ... or with two integers.
        ' '
        >>> board.doMove((1,1))  # 'X' (always first player)
        >>> board[1,1]
        'X'
        >>> board.getWinner()
        '?'
        >>> board.isTerminalPosition()
        False
        >>> print board
             |   |            a | b | c
          ---+---+---        ---+---+---
             | X |            d | e | f
          ---+---+---        ---+---+---
             |   |            g | h | i
        >>> (value, history) = board.alphabeta(-infinity, infinity, [], [])
        >>> value                       # best play from here is a draw.
        0
        >>> history[0:3]                # first three moves in best history
        [(1, 1), (0, 0), (0, 1)]
        >>> board.doMove((0,1)) # 'O'    Again, argument can be point ...
        >>> board.doMove(2,2)   # 'X'    ... or two integers.
        >>> board.doMove(1,0)   # 'O'
        >>> board.doMove(0,0)   # 'X'
        >>> print board
           X | O |            a | b | c
          ---+---+---        ---+---+---
           O | X |            d | e | f
          ---+---+---        ---+---+---
             |   | X          g | h | i
        >>> board.getWinner()            # X has won.
        'X'
        >>> board.isTerminalPosition()
        True
        >>> board.value()                # O's turn; value < 0 means 'bad.'
        -50
        >>> board.nMovesMade()
        5
        >>> board.possibleMoves()
        [(0, 2), (1, 2), (2, 0), (2, 1)]
    """  # the coords of ways to win :
    lines = (((0, 0), (0, 1), (0, 2)),  # 3 horizontal
             ((1, 0), (1, 1), (1, 2)),
             ((2, 0), (2, 1), (2, 2)),
             ((0, 0), (1, 0), (2, 0)),  # 3 vertical
             ((0, 1), (1, 1), (2, 1)),
             ((0, 2), (1, 2), (2, 2)),
             ((0, 0), (1, 1), (2, 2)),  # 2 diagonal
             ((0, 2), (1, 1), (2, 0)))

    def __init__(self):
        self.grid = [[' '] * 3, [' '] * 3, [' '] * 3]
        self.movesMade = []
        self.whoseMove = 'X'
        self._winner = None  # cache for getWinner() result.

    def __str__(self):
        """ Return current board with X's and O's as a string. """
        return self.row2string(0) + "          a | b | c \n" + \
               "  ---+---+---        ---+---+---\n" + \
               self.row2string(1) + "          d | e | f \n" + \
               "  ---+---+---        ---+---+---\n" + \
               self.row2string(2) + "          g | h | i "

    def __getitem__(self, coord, secondArg=None):
        """ Return symbol on board via board[(row,col)] or board[row,col]. """
        if secondArg != None:
            (row, column) = (coord, secondArg)
        else:
            (row, column) = coord
        return self.grid[row][column]

    def nMovesMade(self):
        return len(self.movesMade)

    def row2string(self, row):
        """ Return one row of the board as a string. """
        return "   " + self[row, 0] + " | " + self[row, 1] + " | " + self[row, 2]

    def flipWhoseMove(self):
        self.whoseMove = {'X': 'O', 'O': 'X'}[self.whoseMove]
        self._winner = None

    def getWinner(self):
        """ Return 'X', 'O', 'tie', or (if the game isn't done), '?'. """
        if self._winner: return self._winner
        for line in self.lines:
            marks = list(self[line[i]] for i in (0, 1, 2))
            if (marks[0] in ('X', 'O')) and (marks[0] == marks[1] == marks[2]):
                self._winner = marks[0]
                return self._winner
        if (self.nMovesMade() == 9):
            self._winner = 'tie'
        else:
            self._winner = '?'
        return self._winner

    def alphabeta(self, alpha, beta, alphaHistory, betaHistory):
        """ An implementation of an alpha/beta game tree search. """
        # A pruned min/max search for the best move.
        # * Positive values are good for this player;
        #   negative ones are good for the other player.
        # * Alpha is this player's best previous result;
        #   beta is the other player's best previous result.
        # * Also returned is the move histories matching the alpha/beta values.
        # * The search ends at "terminal nodes", typically
        #   where the game is finished or the search depth is exceeded;
        #   at which point game.isTerminalPosition() is True
        #   and game.value() should give a reasonable value without a search.
        # * The search starts with
        #     (value, history) = alphabeta(gameStart, -inf, inf, [], [])
        # * Based on http://en.wikipedia.org/wiki/Alpha-beta_pruning 2/28/10
        if self.isTerminalPosition():
            return self.value(), self.getHistory()
        for move in self.possibleMoves():
            self.doMove(move)
            (value, history) = self.alphabeta(-beta, -alpha,
                                              betaHistory, alphaHistory)
            self.undoMove(move)
            value = -value  # other player's point of view
            if value > alpha:  # min/max search
                (alpha, alphaHistory) = (value, history)
            if beta <= alpha:  # alpha/beta tree pruning
                break
        return (alpha, alphaHistory)

    def doMove(self, move, secondArg=None):
        """ Place the next player's symbol at move (row,column). """
        if secondArg != None:
            (row, column) = (move, secondArg)
        else:
            (row, column) = move
        self.grid[row][column] = self.whoseMove
        self.movesMade.append((row, column))
        self.flipWhoseMove()

    def undoMove(self, move):
        """ Remove the given last move from the board. """
        (row, column) = move
        self.grid[row][column] = ' '
        self.movesMade.pop()
        self.flipWhoseMove()

    def isTerminalPosition(self):
        """ Return True if the search shouldn't continue past this position. """
        # Tic-Tac-Toe is a simple game; we'll just search all the way to the end.
        return self.getWinner() != '?'

    def getHistory(self):
        """ Return move history. """
        return list(self.movesMade)  # copy it so changes don't propagate out.

    def value(self):
        """ Return the value of a terminal board position. """

        # Positive is good for the player whose turn it is to move.
        # Winning earlier is better; a tie is zero.
        # Otherwise, the formula is arbitrary.
        # At the end of the game, the person to move is typically the loser;
        # the player who made the previous (and last) move has won.
        # So the returned value should be negative, or zero for a draw.
        def losingScore():
            return -10 * (10 - self.nMovesMade())

        return {'tie': lambda: 0,
                'X': losingScore,
                'O': losingScore,
                '?': lambda: None,  # non-terminal position; shouldn't happen.
                }[self.getWinner()]()

    def possibleMoves(self):
        """ Return list of remaining legal move coordinates. """
        # Re-ordering this to put moves more likely be be good earlier
        # will improve the runtime of the alpha/beta pruning algorithm.
        return [(i, j) for i in (0, 1, 2) for j in (0, 1, 2) if self[i, j] == ' ']


class Game(object):
    """ Choose players interactively and play one game, printing each move. """

    def __init__(self, players=[]):
        """ Start a new game with the given players,
            or prompt for the players if not provided."""
        print
        print " == Playing a new game. =="
        if (players):
            self.players = players
        else:
            self.players = [self.askForPlayer('X'), self.askForPlayer('O')]
        self.whoseTurn = 0
        self.board = Board()

    def askForPlayer(self, symbol):
        """ Return a player based on input choice. """
        choices = "user, random, or smart"
        letters = ('u', 's', 'r')
        answer = ask(" Player %s is %s ? " % (symbol, choices), letters)
        return {'u': InteractivePlayer,
                's': SmartPlayer,
                'r': RandomPlayer,
                }[answer[0]](symbol)

    def play(self):
        """ Play one game, printing each move to stdout. """
        print
        winner = '?'
        while (winner == '?'):
            print self.board
            print
            player = self.players[self.whoseTurn]
            nextMove = player.getMove(self.board)
            self.board.doMove(nextMove)
            winner = self.board.getWinner()
            self.whoseTurn = (self.whoseTurn + 1) % 2
        if (winner in ('X', 'O')):
            print self.board
            print
            print " %s wins!" % winner
        else:
            print self.board
            print
            print " Tie game."


class Referee(object):
    """ Run a series of games. """

    def run(self):
        print " === Tic Tac Toe === "
        print " Inputs may be abbreviated by their first letter. "
        print " Type 'quit' at any prompt to quit. "
        print " X always goes first."
        while True:
            Game().play()


def _doctests():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctests()
    Referee().run()
