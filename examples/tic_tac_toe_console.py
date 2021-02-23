from games.tic_tac_toe import TicTacToeGame, SimpleMiniMaxPlayer
from games.game import ConsoleHumanPlayer, Match

aiPlayer = SimpleMiniMaxPlayer('X')
hPlayer = ConsoleHumanPlayer('O')
game = TicTacToeGame(aiPlayer.get_id(), hPlayer.get_id())
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
