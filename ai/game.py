from abc import ABC, abstractmethod
from minmaxm import find_best_move

#============================================================================
# Game class
#============================================================================
class Game(ABC):
    def __init__(self, gameName):
        super().__init__()
        self.gameName = gameName

    @abstractmethod
    def evaluate(self, actual_depth):
        pass

    @abstractmethod    
    def check_win(self, player):
        pass

    @abstractmethod
    def is_moves_left(self):
        pass

    @abstractmethod
    def valid_moves(self):
        pass

    @abstractmethod
    def depth(self):
        pass

    @abstractmethod
    def do_move(self, move, player):
        pass

    @abstractmethod    
    def undo(self):
        pass

    @abstractmethod    
    def to_string(self):
        pass

#============================================================================
# Base Player class
#============================================================================
class Player(ABC):
    def __init__(self, symbol, maximizingPlayer):
        self.symbol = symbol
        self.maximizingPlayer = maximizingPlayer

    def get_symbol(self):
        return self.symbol

    def is_max(self):
        return self.maximizingPlayer

    @abstractmethod
    def do_move(self, board):
        pass

#============================================================================
# AIMaxPlayer class
#============================================================================
class AIMaxPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol, True)

    def do_move(self, board):
        _, move = find_best_move(board)
        if move is not None:
            board.do_move(move, self.maximizingPlayer)

#============================================================================
# ConsoleHumanPlayer class
#============================================================================
class ConsoleHumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol, False)

    def do_move(self, board):
        print(board.to_string())
        while True:
            try:
                choice = int(input("make your move : "))
                board.do_move(choice, self.maximizingPlayer)
                break
            except Exception:
                print('Please, peek a valid move...')

#============================================================================
# Match class
#============================================================================
DRAW = 'Draw'

class Match():
    def __init__(self, game, firstPlayer, secondPlayer):
        self.game = game
        self.players = [firstPlayer, secondPlayer]

    def run(self):
        gameover = False
        while not gameover:
            for player in self.players:
                player.do_move(self.game)

                if not self.game.is_moves_left():
                    gameover = True
                    break
                if self.game.check_win(player.is_max()):
                    gameover = True
                    break

        for player in self.players:
            if self.game.check_win(player.is_max()):
                return player.get_symbol()
        
        return DRAW
        


