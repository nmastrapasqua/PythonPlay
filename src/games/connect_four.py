#=============================================================================
# Origin:
# https://gist.github.com/poke/6934842
#=============================================================================

from games.game import Game, Player
from queue import LifoQueue
from games.exception import MoveNotAllowedException
from itertools import groupby, chain
import numpy as np


#============================================================================
# Class ConnectFourGame
#============================================================================
class ConnectFourGame(Game):
    def __init__(self, player1, player2, rows = 6, cols = 7):
        super().__init__("Connect Four")
        self.board = np.zeros((rows, cols))
        self.undo_stack = LifoQueue()
        self.player1 = player1
        self.player2 = player2
        self.rows = rows
        self.cols = cols

    def get_opponent(self, playerId):
        return self.player2 if self.player1 == playerId else self.player1

    def get_board(self):
        return self.board

    def check_win(self, playerId):
        # Check horizontal locations for win
        for c in range(self.cols-3):
            for r in range(self.rows):
                if self.board[r][c] == playerId and self.board[r][c+1] == playerId and self.board[r][c+2] == playerId and self.board[r][c+3] == playerId:
                    return True

        # Check vertical locations for win
        for c in range(self.cols):
            for r in range(self.rows-3):
                if self.board[r][c] == playerId and self.board[r+1][c] == playerId and self.board[r+2][c] == playerId and self.board[r+3][c] == playerId:
                    return True

        # Check positively sloped diaganols
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == playerId and self.board[r+1][c+1] == playerId and self.board[r+2][c+2] == playerId and self.board[r+3][c+3] == playerId:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == playerId and self.board[r-1][c+1] == playerId and self.board[r-2][c+2] == playerId and self.board[r-3][c+3] == playerId:
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