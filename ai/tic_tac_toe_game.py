#=============================================================================
# heuristic from:
# https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-tic-tac-toe/
#=============================================================================
from game import Game
from queue import LifoQueue
from exception import MoveNotAllowedException

EMPTY = '_'

TURN_PENALITY = 50

THREE_IN_A_ROW = [
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ]]

HEURISTIC = [
    [     0,   -10,  -100, -1000 ],
    [    10,     0,     0,     0 ],
    [   100,     0,     0,     0 ],
    [  1000,     0,     0,     0 ]]

#============================================================================
# Class Player
#============================================================================
class Player():
    def __init__(self, symbol, maximizingPlayer):
         self.symbol = symbol
         self.maximizingPlayer = maximizingPlayer

    def get_symbol(self):
        return self.symbol

    def is_maximizing_player(self):
        return self.maximizingPlayer

    def get_move(self, board):
        pass

#============================================================================
# Class TicTacToeGame
#============================================================================
class TicTacToeGame(Game):
    def __init__(self, player1, player2, max_depth=3):
        super().__init__("Tic Tac Toe")
        self.board = [EMPTY for i in range(0, 9)]
        self.max_depth = max_depth
        self.undo_stack = LifoQueue()
        self.isMaximizingTurn = None
        self.symbolMap = {
            player1.is_maximizing_player(): player1.get_symbol(), 
            player2.is_maximizing_player(): player2.get_symbol()
        }

    def turn(self, player):
        self.isMaximizingTurn = player.is_maximizing_player()

    def evaluate(self, player):
        player_sym = self.symbolMap[player]
        opponent_sym = self.symbolMap[not player]
        piece = None
        t = 0

        for i in range(0, 8):
            players, others = 0, 0
            for j in range(0, 3):
                piece = self.board[THREE_IN_A_ROW[i][j]]
                if piece == player_sym:
                    players += 1
                elif piece == opponent_sym:
                    others += 1
            t += HEURISTIC[players][others]

        return t if not player == self.isMaximizingTurn else t - TURN_PENALITY

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