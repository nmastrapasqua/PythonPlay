#=======================================================================================
# Origin: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/?ref=lbp
# Python3 program to demonstrate 
# working of Alpha-Beta Pruning 
#=======================================================================================
import math

# Initial values of Aplha and Beta 
MAX, MIN = math.inf, -math.inf

#=======================================================================================
# Returns optimal value for current player 
#(Initially called for root and maximizer) 
#=======================================================================================
def minimax(game, depth, maximizingPlayer, alpha, beta): 
	score = game.evaluate()

	# If Maximizer has won the game return his/her 
    # evaluated score 
	if game.check_win(True):
		return score

	# If Minimizer has won the game return his/her 
    # evaluated score 
	if game.check_win(False):
		return score 

	# If there are no more moves and no winner then 
    # it is a tie
	if not game.is_moves_left():
		return score

	# Terminating condition. i.e 
	# max depth is reached 
	if depth == game.depth(): 
		return score 

	if maximizingPlayer: 
	
		best = MIN

		# Recur for valid moves 
		for move in game.valid_moves(): 
			# Make the move 
			game.do_move(move, True)

			val = minimax(game, depth + 1, False, alpha, beta) 
			best = max(best, val) 
			alpha = max(alpha, best) 

			# Undo the move 
			game.undo()

			# Alpha Beta Pruning 
			if beta <= alpha: 
				break
		
		return best 
	
	else: 
		best = MAX

		# Recur for valid moves 
		for move in game.valid_moves(): 
			# Make the move 
			game.do_move(move, False)

			val = minimax(game, depth + 1, True, alpha, beta) 
			best = min(best, val) 
			beta = min(beta, best) 

			# Undo the move 
			game.undo()

			# Alpha Beta Pruning 
			if beta <= alpha: 
				break
		
		return best 

#=======================================================================================
# This will return the best possible move for the player 
#=======================================================================================
def find_best_move(game):
	bestVal = -math.inf
	bestMove = None

	for move in game.valid_moves():
		game.do_move(move, True)
		moveVal = minimax(game, 0, False, -math.inf, math.inf)
		game.undo()
		if moveVal > bestVal:
			bestMove = move
			bestVal = moveVal

	return bestVal, bestMove
