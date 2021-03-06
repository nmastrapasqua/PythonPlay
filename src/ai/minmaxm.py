#=======================================================================================
# Origin: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/?ref=lbp
# Python3 program to demonstrate 
# working of Alpha-Beta Pruning 
#=======================================================================================
import math

# Initial values of Aplha and Beta 
MAX, MIN = math.inf, -math.inf

#=======================================================================================
# MiniMax class 
#=======================================================================================
class MiniMax():
	def __init__(self, playerId, eval, max_depth):
		self.playerId = playerId
		self.eval = eval
		self.max_depth = max_depth

	def minimax(self, game, depth, maximizingPlayer, alpha, beta):
		opponentId = game.get_opponent(self.playerId)
		score = self.eval(game, depth)

		# If Maximizer has won the game return his/her 
		# evaluated score 
		if game.check_win(self.playerId):
			return score

		# If Minimizer has won the game return his/her 
		# evaluated score 
		if game.check_win(opponentId):
			return score 

		# If there are no more moves and no winner then 
		# it is a tie
		if not game.is_moves_left():
			return score

		# Terminating condition. i.e 
		# max depth is reached 
		if depth == self.max_depth: 
			return score 

		if maximizingPlayer: 
			best = MIN

			# Recur for valid moves 
			for move in game.valid_moves(): 
				# Make the move 
				game.do_move(move, self.playerId)

				val = self.minimax(game, depth + 1, False, alpha, beta) 
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
				game.do_move(move, opponentId)

				val = self.minimax(game, depth + 1, True, alpha, beta) 
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
	def find_best_move(self, game):
		bestVal = -math.inf
		bestMove = None

		for move in game.valid_moves():
			game.do_move(move, self.playerId)
			moveVal = self.minimax(game, 0, False, -math.inf, math.inf)
			game.undo()
			if moveVal > bestVal:
				bestMove = move
				bestVal = moveVal

		return bestVal, bestMove
