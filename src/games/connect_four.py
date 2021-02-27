#=============================================================================
# Origin:
# https://www.youtube.com/watch?v=XpYz-q1lxu8
#=============================================================================

from games.game import Game, Player
from queue import LifoQueue
from games.exception import MoveNotAllowedException
import numpy as np
from ai.minmaxm import MiniMax

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
DRAW = 3
WIN_SCORE = 100000

#============================================================================
# MiniMaxPlayer class for Connect Four Game
#============================================================================
class MiniMaxPlayer(Player):
    def __init__(self, id, max_depth=2):
        super().__init__(id)
        self.minimax = MiniMax(self.id, self.evaluate, max_depth)

    def do_move(self, game):
        _, move = self.minimax.find_best_move(game)
        if move is not None:
            game.do_move(move, self.id)
        return move

    def evaluate(self, game, actual_depth):
        return self.eval1(game, actual_depth)

    def eval1(self, game, actual_depth):
        opponentId = game.get_opponent(self.id)
        fourInRow = 0
        threeInRow = 0
        twoInRow = 0

        if game.check_win(opponentId):
            return -WIN_SCORE

        for window in game.get_windows():
            fourInRow += self.count(window, self.id, 4)
            threeInRow += self.count(window, self.id, 3)
            twoInRow += self.count(window, self.id, 2)
            
        return WIN_SCORE*fourInRow + 100*threeInRow + twoInRow

    def count(self, window, playerId, size):
        if window.count(playerId) == size and window.count(EMPTY) == len(window) - size:
            return 1
        return 0

#============================================================================
# Class ConnectFourGame
#============================================================================
class ConnectFourGame(Game):
    def __init__(self, player1, player2, rows = 6, cols = 7, window_length = 4):
        super().__init__("Connect Four")
        self.board = np.zeros((rows, cols), dtype=int)
        self.undo_stack = LifoQueue()
        self.player1 = player1
        self.player2 = player2
        self.rows = rows
        self.cols = cols
        self.window_length = window_length

    def get_opponent(self, playerId):
        return self.player2 if self.player1 == playerId else self.player1

    def get_board(self):
        return self.board

    def check_win(self, playerId):
        for window in self.get_windows():
            if window.count(playerId) == self.window_length:
                return True

        return False

    def is_moves_left(self):
        return len(self.valid_moves()) > 0

    def valid_moves(self):
        valid_locations = []
        for col in range(self.cols):
            if self.board[self.rows-1][col] == 0:
                valid_locations.append(col)
        return valid_locations

    def do_move(self, move, playerId):
        row = None
        for r in range(self.rows):
            if self.board[r][move] == 0:
                row = r
                break

        if row is None:
            raise MoveNotAllowedException('Column is full')

        self.undo_stack.put({'col' : move, 'row': row, 'symbol' : self.board[row][move]})
        self.board[row][move] = playerId

    def undo(self):
        previous = self.undo_stack.get()
        col = previous['col']
        row = previous['row']
        piece = previous['symbol']
        self.board[row][col] = piece

    def to_string(self):
        #Print the board.
        result = np.flip(self.board, 0)
        return result

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_center_column(self):
        return [int(i) for i in list(self.board[:, self.cols//2])]

    def get_windows(self):
        windows = []

        ## Score Horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r,:])]
            for c in range(self.cols-3):
                windows.append(row_array[c:c+self.window_length])

        ## Score Vertical
        for c in range(self.cols):
            col_array = [int(i) for i in list(self.board[:,c])]
            for r in range(self.rows-3):
                windows.append(col_array[r:r+self.window_length])

        ## Score posiive sloped diagonal
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                windows.append([self.board[r+i][c+i] for i in range(self.window_length)])
                

        for r in range(self.rows-3):
            for c in range(self.cols-3):
               windows.append([self.board[r+3-i][c+i] for i in range(self.window_length)])

        return windows
                