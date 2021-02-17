from abc import ABC, abstractmethod
import random

#============================================================================
# Game class
#============================================================================
class Game(ABC):
    def __init__(self, gameName):
        super().__init__()
        self.gameName = gameName

    @abstractmethod
    def get_opponent(self, playerId):
        pass

    @abstractmethod    
    def check_win(self, playerId):
        pass

    @abstractmethod
    def is_moves_left(self):
        pass

    @abstractmethod
    def valid_moves(self):
        pass

    @abstractmethod
    def do_move(self, move, playerId):
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
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    @abstractmethod
    def do_move(self, board):
        pass

    @abstractmethod
    def evaluate(self, board, actual_depth):
        pass

#============================================================================
# ConsoleHumanPlayer class
#============================================================================
class ConsoleHumanPlayer(Player):
    def __init__(self, id):
        super().__init__(id)

    def do_move(self, board):
        print(board.to_string())
        while True:
            try:
                choice = int(input("make your move : "))
                board.do_move(choice, self.id)
                break
            except Exception:
                print('Please, peek a valid move...')

    def evaluate(self, board, actual_depth):
        return 0

#============================================================================
# RandomPlayer class
#============================================================================
class RandomPlayer(Player):
    def __init__(self, id):
        super().__init__(id)

    def do_move(self, board):
        moves = board.valid_moves()
        if moves is None or len(moves) == 0:
            return
        index = random.randint(0, len(moves)-1)
        move = moves[index]
        board.do_move(move, self.id)
        
    def evaluate(self, board, actual_depth):
        return 0

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
                if self.game.check_win(player.get_id()):
                    gameover = True
                    break

        for player in self.players:
            if self.game.check_win(player.get_id()):
                return player.get_id()
        
        return DRAW
        


