#=============================================================================
# heuristic from:
# https://www.youtube.com/watch?v=trKjYdBASyQ
#=============================================================================
from game import Game
from queue import LifoQueue
from exception import MoveNotAllowedException
import math

EMPTY = '_'

THREE_IN_A_ROW = [
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ]]

#============================================================================
# Class TicTacToeGame
#============================================================================
class TicTacToeGame(Game):
    def __init__(self, maxSymbol, minSymbol, max_depth=math.inf):
        super().__init__("Tic Tac Toe")
        self.board = [EMPTY for i in range(0, 9)]
        self.max_depth = max_depth
        self.undo_stack = LifoQueue()
        self.symbolMap = {
            True  : maxSymbol, 
            False : minSymbol
        }

    def evaluate(self, actual_depth):
        if self.check_win(True):
            return 10 - actual_depth
        elif self.check_win(False):
            return -10 + actual_depth
        else:
            return 0

    def check_win(self, player):
        player_sym = self.symbolMap[player]
        piece = None

        for i in range(0, 8):
            players = 0
            for j in range(0, 3):
                piece = self.board[THREE_IN_A_ROW[i][j]]
                if piece == player_sym:
                    players += 1
                    if players == 3:
                        return True

        return False

    def is_moves_left(self):
        try:
            self.board.index(EMPTY)
            return True
        except ValueError:
            return False

    def valid_moves(self):
        return [i for i, e in enumerate(self.board) if e == EMPTY]
        
    def depth(self):
        return self.max_depth

    def do_move(self, move, player):
        if not self.board[move] == EMPTY:
            raise MoveNotAllowedException(f"The position on the board is occupied by {self.board[move]}")
        self.undo_stack.put({'move' : move, 'symbol' : self.board[move]})
        self.board[move] = self.symbolMap[player]

    def undo(self):
        previous = self.undo_stack.get()
        self.board[previous['move']] = previous['symbol']

    def to_string(self):
        str = ''
        for i in range (0, 9):
            str += self.board[i]
            str += ' '
            if (i+1) % 3 == 0:
                str += '\n'
        return str