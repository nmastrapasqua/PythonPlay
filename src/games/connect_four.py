#=============================================================================
# Origin:
# https://gist.github.com/poke/6934842
#=============================================================================

from games.game import Game, Player
from queue import LifoQueue
from games.exception import MoveNotAllowedException
from itertools import groupby, chain

NONE = '.'

#============================================================================
# Class ConnectFourGame
#============================================================================
class ConnectFourGame(Game):
    def __init__(self, player1, player2, cols = 7, rows = 6, requiredToWin = 4):
        super().__init__("Connect Four")
        self.board = [[NONE] * rows for _ in range(cols)]
        self.undo_stack = LifoQueue()
        self.player1 = player1
        self.player2 = player2
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin

    def get_opponent(self, playerId):
        return self.player2 if self.player1 == playerId else self.player1

    def get_board(self):
        return self.board

    def check_win(self, playerId):
        if self.get_winner():
            return self.get_winner() == playerId
        return False

    def is_moves_left(self):
        return len(self.valid_moves()) > 0

    def valid_moves(self):
        moves = []
        last_pos = 0
        for col in self.board:
            if col[0] == NONE:
                moves.append(self.board.index(col, last_pos))
            last_pos += 1
        return moves

    def do_move(self, move, playerId):
        #Insert the color in the given column.
        c = self.board[move]
        if c[0] != NONE:
            raise MoveNotAllowedException('Column is full')

        i = -1
        while c[i] != NONE:
            i -= 1
        self.undo_stack.put({'col' : move, 'row': i, 'symbol' : self.board[move][i]})
        c[i] = playerId

    def undo(self):
        previous = self.undo_stack.get()
        col = previous['col']
        row = previous['row']
        piece = previous['symbol']
        self.board[col][row] = piece

    def to_string(self):
        #Print the board.
        result = '  '.join(map(str, range(self.cols)))
        result += '\n'
        for y in range(self.rows):
            result += '  '.join(str(self.board[x][y]) for x in range(self.cols))
            result += '\n'
        return result

    def diagonals_pos(self):
	    # Get positive diagonals, going from bottom-left to top-right.
	    for di in ([(j, i - j) for j in range(self.cols)] for i in range(self.cols + self.rows -1)):
		    yield [self.board[i][j] for i, j in di if i >= 0 and j >= 0 and i < self.cols and j < self.rows]

    def diagonals_neg(self):
	    # Get negative diagonals, going from top-left to bottom-right.
	    for di in ([(j, i - self.cols + j + 1) for j in range(self.cols)] for i in range(self.cols + self.rows - 1)):
		    yield [self.board[i][j] for i, j in di if i >= 0 and j >= 0 and i < self.cols and j < self.rows]

    def get_winner(self):
		#Get the winner on the current board.
        lines = (
			self.board, # columns
			zip(*self.board), # rows
			self.diagonals_pos(), # positive diagonals
			self.diagonals_neg() # negative diagonals
		)

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

        return None