from tic_tac_toe_game import TicTacToeGame
from game import AIMaxPlayer, ConsoleHumanPlayer, Match

aiPlayer = AIMaxPlayer('X')
hPlayer = ConsoleHumanPlayer('O')
game = TicTacToeGame(aiPlayer.get_symbol(), hPlayer.get_symbol())
match = None

first_player = str(input("First player (x/o) : "))
players = [aiPlayer]
if first_player == 'x':
    match = Match(game, aiPlayer, hPlayer)
else:
    match = Match(game, hPlayer, aiPlayer)
    
outcome = match.run()
print(game.to_string())
print(f'Winner is : {outcome}')
