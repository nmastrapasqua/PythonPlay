from tic_tac_toe_game import TicTacToeGame, Player
from minmaxm import find_best_move

class HumanPlayer(Player):
    def __init__(self, symbol, maximizingPlayer):
        super().__init__(symbol, maximizingPlayer)

    def get_move(self, board):
        print(board.to_string())
        print(f'Human={board.evaluate(self.maximizingPlayer)} - AI={board.evaluate(not self.maximizingPlayer)}')
        print("make your move:")
        choice = int(input())
        return choice

class AIPlayer(Player):
    def __init__(self, symbol, maximizingPlayer):
        super().__init__(symbol, maximizingPlayer)

    def get_move(self, board):
        _, move = find_best_move(board)
        return move

aiPlayer = AIPlayer('O', True)
hPlayer = HumanPlayer('X', False)
game = TicTacToeGame(aiPlayer, hPlayer, 3)

while True:

    game.turn(hPlayer)
    move = hPlayer.get_move(game)
    game.do_move(move, hPlayer.is_maximizing_player())

    game.turn(aiPlayer)
    move = aiPlayer.get_move(game)
    if move is not None:
        game.do_move(move, aiPlayer.is_maximizing_player())

    if not game.is_moves_left():
        break
    if game.check_win(hPlayer.is_maximizing_player()):
        break
    if game.check_win(aiPlayer.is_maximizing_player()):
        break

print(game.to_string())
if game.check_win(hPlayer.is_maximizing_player()):
    print('Human won')
elif game.check_win(aiPlayer.is_maximizing_player()):
    print('Computer won')
else:
    print('Draw game')