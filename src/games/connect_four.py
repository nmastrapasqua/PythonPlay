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
WIN_SCORE = 100000000000000

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
        opponentId = game.get_opponent(self.id)

        if game.check_win(self.id):
            return WIN_SCORE

        elif game.check_win(opponentId):
            return -WIN_SCORE

        else:
            return self.score_position(game)

    def score_position(self, game):
        board = game.get_board()
        score = 0
        window_len = game.get_window_length()

        ## Score center column
        center_array = [int(i) for i in list(board[:, game.get_cols()//2])]
        center_count = center_array.count(self.id)
        score += center_count * 3

        ## Score Horizontal
        for r in range(game.get_rows()):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(game.get_cols()-3):
                window = row_array[c:c+window_len]
                score += self.evaluate_window(window, game)

        ## Score Vertical
        for c in range(game.get_cols()):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(game.get_rows()-3):
                window = col_array[r:r+window_len]
                score += self.evaluate_window(window, game)

        ## Score posiive sloped diagonal
        for r in range(game.get_rows()-3):
            for c in range(game.get_cols()-3):
                window = [board[r+i][c+i] for i in range(window_len)]
                score += self.evaluate_window(window, game)

        for r in range(game.get_rows()-3):
            for c in range(game.get_cols()-3):
                window = [board[r+3-i][c+i] for i in range(window_len)]
                score += self.evaluate_window(window, game)

        return score

    def evaluate_window(self, window, game):
        score = 0
        opp_piece = game.get_opponent(self.id)

        if window.count(self.id) == 4:
            score += 100
        elif window.count(self.id) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(self.id) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

#============================================================================
# Class ConnectFourGame
#============================================================================
class ConnectFourGame(Game):
    def __init__(self, player1, player2, rows = 6, cols = 7, window_length = 4):
        super().__init__("Connect Four")
        self.board = np.zeros((rows, cols))
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

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_window_length(self):
        return self.window_length