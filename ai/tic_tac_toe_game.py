#=============================================================================
# heuristic from:
# https://www.youtube.com/watch?v=trKjYdBASyQ
#=============================================================================
from game import Game, Player
from queue import LifoQueue
from exception import MoveNotAllowedException
import math
from minmaxm import MiniMax

#============================================================================
# SimpleMiniMaxPlayer class for Tic Tac Toe Game
#============================================================================
class SimpleMiniMaxPlayer(Player):
    def __init__(self, id):
        super().__init__(id)
        self.minimax = MiniMax(self.id, self.evaluate, math.inf)

    def do_move(self, board):
        _, move = self.minimax.find_best_move(board)
        if move is not None:
            board.do_move(move, self.id)

    def evaluate(self, board, actual_depth):
        if board.check_win(self.id):
            return 10 - actual_depth
        elif board.check_win(board.get_opponent(self.id)):
            return -10 + actual_depth
        else:
            return 0


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
    def __init__(self, player1, player2):
        super().__init__("Tic Tac Toe")
        self.board = [EMPTY for i in range(0, 9)]
        self.undo_stack = LifoQueue()
        self.player1 = player1
        self.player2 = player2

    def get_opponent(self, playerId):
        return self.player2 if self.player1 == playerId else self.player1

    def check_win(self, playerId):
        piece = None

        for i in range(0, 8):
            players = 0
            for j in range(0, 3):
                piece = self.board[THREE_IN_A_ROW[i][j]]
                if piece == playerId:
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

    def do_move(self, move, playerId):
        if not self.board[move] == EMPTY:
            raise MoveNotAllowedException(f"The position on the board is occupied by {self.board[move]}")
        self.undo_stack.put({'move' : move, 'symbol' : self.board[move]})
        self.board[move] = playerId

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