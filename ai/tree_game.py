from game import Game
from queue import LifoQueue
import math

#============================================================================
# class TreeGame
#============================================================================
class TreeGame(Game):
    def __init__(self, name, startState, transactions, max_depth):
        super().__init__(name)
        self.status = startState
        self.transactions = transactions
        self.max_depth = max_depth
        self.undo_stack = LifoQueue()

    def get_status(self):
        return self.status

    def get_opponent(self, playerId):
        return None

    def check_win(self, playerId):
        return False

    def is_moves_left(self):
        return self.status in self.transactions

    def valid_moves(self):
        return self.transactions[self.status]
        
    def depth(self):
        return self.max_depth

    def do_move(self, move, playerId):
        self.undo_stack.put(self.status)
        self.status = self.transactions[self.status][move]

    def undo(self):
        self.status = self.undo_stack.get()

    def to_string(self):
        return f'{self.gameName} : Status = {self.status}, eval={self.evaluate()}, max_depth={self.max_depth}'


#============================================================================
# Moves
#============================================================================
LT = 'LEFT'
CT = 'CENTER'
RT = 'RIGHT'

#============================================================================
# See image tree_1.png
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/?ref=lbp
#============================================================================
heuristic_1 = {
            'H':3,
            'I':5,
            'L':6,
            'M':9,
            'N':1,
            'O':2,
            'P':0,
            'Q':-1
        }

def eval_1(board, actual_depth):
    return heuristic_1.get(board.get_status(), 0)

def get_tree_1_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        'A' : {LT :'B', RT :'C'},
        'B' : {LT :'D', RT :'E'},
        'C' : {LT :'F', RT :'G'},
        'D' : {LT :'H', RT :'I'},
        'E' : {LT :'L', RT :'M'},
        'F' : {LT :'N', RT :'O'},
        'G' : {LT :'P', RT :'Q'}
    }
    
    expected_sore = 5
    expected_move = LT
    return TreeGame("Test 1", "A", transactions, 3), expected_sore, expected_move, eval_1

#============================================================================
# See image tree_2.png
# https://www.javatpoint.com/ai-alpha-beta-pruning
#============================================================================
heuristic_2 = {
            'H':2,
            'I':3,
            'L':5,
            'M':9,
            'N':0,
            'O':1,
            'P':7,
            'Q':5
        }

def eval_2(board, actual_depth):
    return heuristic_2.get(board.get_status(), 0)

def get_tree_2_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        'A' : {LT :'B', RT :'C'},
        'B' : {LT :'D', RT :'E'},
        'C' : {LT :'F', RT :'G'},
        'D' : {LT :'H', RT :'I'},
        'E' : {LT :'L', RT :'M'},
        'F' : {LT :'N', RT :'O'},
        'G' : {LT :'P', RT :'Q'}
    }
    
    expected_sore = 3
    expected_move = LT
    return TreeGame("Test 2", "A", transactions, 3), expected_sore, expected_move, eval_2

#============================================================================
# See image tree_3.png
# http://www.paoloferraresi.it/mydocs/articoli/minimax.pdf
#============================================================================
heuristic_3 = {
            '21':9,
            '22':8,
            '23':7,
            '24':6,
            '25':5,
            '26':4,
            '27':3,
            '28':2,
            '29':1
        }

def eval_3(board, actual_depth):
    return heuristic_3.get(board.get_status(), 0)

def get_tree_3_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        '01' : {LT :'11', CT: '12', RT :'13'},
        '11' : {LT :'21', CT: '22', RT :'23'},
        '12' : {LT :'24', CT: '25', RT :'26'},
        '13' : {LT :'27', CT: '28', RT :'29'}
    }
    
    expected_score = 7
    expected_move = LT
    return TreeGame("Test 3", "01", transactions, 2), expected_score, expected_move, eval_3


#============================================================================
# See image tree_4.png
# http://lia.deis.unibo.it/Courses/AI/Lucidi/giochi-es.pdf
#============================================================================
heuristic_4 = {
            'K':6,
            'L':8,
            'M':5,
            'N':0,
            'O':-2,
            'P':2,
            'Q':5,
            'R':8,
            'S':9,
            'T':2,
            'U':0
        }
def eval_4(board, actual_depth):
    return heuristic_4.get(board.get_status(), 0)

def get_tree_4_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        'A' : {LT :'B', CT: 'C', RT :'D'},
        'B' : {LT :'E', RT :'F'},
        'C' : {LT :'G', RT :'H'},
        'D' : {LT :'I', RT :'J'},
        'E' : {LT :'K'},
        'F' : {LT :'L', RT :'M'},
        'G' : {LT :'N', RT :'O'},
        'H' : {LT :'P', RT :'Q'},
        'I' : {LT :'R', RT :'S'},
        'J' : {LT :'T', RT :'U'}
    }
    
    expected_score = 6
    expected_move = LT
    return TreeGame("Test 4", "A", transactions, 3), expected_score, expected_move, eval_4

#============================================================================
# See image tree_5.png
# https://www.youtube.com/watch?app=desktop&v=Ewh-rF7KSEg
#============================================================================
heuristic_5 = {
            'E':4,
            'F':5,
            'G':6,
            'M':3,
            'N':4,
            'O':7,
            'P':9,
            'K':3,
            'L':8
        }
def eval_5(board, actual_depth):
    return heuristic_5.get(board.get_status(), 0)

def get_tree_5_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        'A' : {LT :'B', CT: 'C', RT :'D'},
        'B' : {LT :'E', RT :'F'},
        'C' : {LT :'G', CT :'H', RT: 'J'},
        'D' : {LT :'K', RT :'L'},
        'H' : {LT :'M', RT :'N'},
        'J' : {LT :'O', RT :'P'}
    }
    
    expected_score = 4
    expected_move = LT
    return TreeGame("Test 5", "A", transactions, math.inf), expected_score, expected_move, eval_5

#============================================================================
# See image tree_6.png
# http://homepage.ufp.pt/jtorres/ensino/ia/alfabeta.html
#============================================================================
heuristic_6 = {
            'E':-1,
            'F':0,
            'G':-10,
            'H':2,
            'I':4,
            'L':6,
            'M':14,
            'N':5,
            'O':70
        }

def eval_6(board, actual_depth):
    return heuristic_6.get(board.get_status(), 0)

def get_tree_6_game():
    # currentState : {move1 : nextState1, move2 : nextState2}
    transactions = {
        'A' : {LT :'B', CT: 'C', RT :'D'},
        'B' : {LT :'E', CT: 'F', RT :'G'},
        'C' : {LT :'H', CT: 'I', RT :'L'},
        'D' : {LT :'M', CT: 'N', RT :'O'}
    }
    
    expected_score = 5
    expected_move = RT
    return TreeGame("Test 6", "A", transactions, 2), expected_score, expected_move, eval_6
