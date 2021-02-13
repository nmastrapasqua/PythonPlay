from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, gameName):
        super().__init__()
        self.gameName = gameName

    @abstractmethod
    def evaluate(self, player):
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
