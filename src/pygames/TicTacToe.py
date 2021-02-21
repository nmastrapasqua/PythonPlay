#======================================================================
# Origin:
# https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/
#======================================================================
# importing the required libraries 
import pygame as pg 
import sys 
import time 
import random
from pygame.locals import *
import numpy as np
from games.tic_tac_toe_game import SimpleMiniMaxPlayer, TicTacToeGame
import os

# declaring the global variables 

# for storing the 'x' or 'o' 
# value as character 
XO = None

# storing the winner's value at 
# any instant of code 
winner = None

# to check if the game is a draw 
draw = None

# to set width of the game window 
width = 400

# to set height of the game window 
height = 400

# to set background color of the 
# game window 
white = (255, 255, 255) 

# color of the straightlines on that 
# white game board, dividing board 
# into 9 parts 
line_color = (0, 0, 0) 

# setting up a 3 * 3 board in canvas 
board = [[None]*3, [None]*3, [None]*3] 


# initializing the pygame window 
pg.init() 

# setting fps manually 
fps = 30

# this is used to track time 
CLOCK = pg.time.Clock() 

# this method is used to build the 
# infrastructure of the display 
screen = pg.display.set_mode((width, height + 100), 0, 32) 

# setting up a nametag for the 
# game window 
pg.display.set_caption("My Tic Tac Toe") 

# Media path
MEDIA_PATH = f'{os.getcwd()}/src/pygames/images/tictactoe'

# loading the images as python object 
initiating_window = pg.image.load(f"{MEDIA_PATH}/modified_cover.png") 
x_img = pg.image.load(f"{MEDIA_PATH}/X_modified.png") 
y_img = pg.image.load(f"{MEDIA_PATH}/o_modified.png") 

# resizing images 
initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

HUMAN = 'o'
COMPUTER = 'x'
DIFFICULTY = 10
computerPlayer = SimpleMiniMaxPlayer(COMPUTER, DIFFICULTY)

def game_initiating_window(startup): 
	
	if startup:
		# displaying over the screen 
		screen.blit(initiating_window, (0, 0)) 
	
		# updating the display 
		pg.display.update() 
		time.sleep(3)

	screen.fill(white) 

	# drawing vertical lines 
	pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
	pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

	# drawing horizontal lines 
	pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
	pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

def draw_status(): 
	
	# getting the global variable draw 
	# into action 
	global draw 
	
	if winner is None: 
		message = "Computer's Turn" if XO == COMPUTER else "Human's Turn"
	else: 
		message = "Computer won !" if XO == COMPUTER else "Human won !"
	if draw: 
		message = "Game Draw !"

	# setting a font object 
	font = pg.font.Font(None, 30) 
	
	# setting the font properties like 
	# color and width of the text 
	text = font.render(message, 1, (255, 255, 255)) 

	# copy the rendered message onto the board 
	# creating a small block at the bottom of the main display 
	screen.fill ((0, 0, 0), (0, 400, 500, 100)) 
	text_rect = text.get_rect(center =(width / 2, 500-50)) 
	screen.blit(text, text_rect) 
	pg.display.update() 
	
def check_win(): 
	global board, winner, draw 

	# checking for winning rows 
	for row in range(0, 3): 
		if((board[row][0] == board[row][1] == board[row][2]) and (board [row][0] is not None)): 
			winner = board[row][0] 
			pg.draw.line(screen, (250, 0, 0), 
						(0, (row + 1)*height / 3 -height / 6), 
						(width, (row + 1)*height / 3 - height / 6 ), 
						4) 
			break

	# checking for winning columns 
	for col in range(0, 3): 
		if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)): 
			winner = board[0][col] 
			pg.draw.line (screen, (250, 0, 0), ((col + 1)* width / 3 - width / 6, 0), \
						((col + 1)* width / 3 - width / 6, height), 4) 
			break

	# check for diagonal winners 
	if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None): 
		
		# game won diagonally left to right 
		winner = board[0][0] 
		pg.draw.line (screen, (250, 70, 70), (50, 50), (350, 350), 4) 
		
	if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None): 
		
		# game won diagonally right to left 
		winner = board[0][2] 
		pg.draw.line (screen, (250, 70, 70), (350, 50), (50, 350), 4) 

	if(all([all(row) for row in board]) and winner is None ): 
		draw = True
	
def drawXO(row, col): 
	global board, XO 
	
	# for the first row, the image 
	# should be pasted at a x coordinate 
	# of 30 from the left margin 
	if row == 1: 
		posx = 30
		
	# for the second row, the image 
	# should be pasted at a x coordinate 
	# of 30 from the game line	 
	if row == 2: 

		# margin or width / 3 + 30 from 
		# the left margin of the window 
		posx = width / 3 + 30
		
	if row == 3: 
		posx = width / 3 * 2 + 30

	if col == 1: 
		posy = 30
		
	if col == 2: 
		posy = height / 3 + 30
	
	if col == 3: 
		posy = height / 3 * 2 + 30
		
	# setting up the required board 
	# value to display 
	board[row-1][col-1] = XO 
	
	if(XO == COMPUTER): 
		
		# pasting x_img over the screen 
		# at a coordinate position of 
		# (pos_y, posx) defined in the 
		# above code 
		screen.blit(x_img, (posy, posx)) 
	
	else: 
		screen.blit(o_img, (posy, posx)) 
	
	pg.display.update() 

def user_click(): 
	# get coordinates of mouse click 
	x, y = pg.mouse.get_pos() 

	# get column of mouse click (1-3) 
	if(x<width / 3): 
		col = 1
	
	elif (x<width / 3 * 2): 
		col = 2
	
	elif(x<width): 
		col = 3
	
	else: 
		col = None

	# get row of mouse click (1-3) 
	if(y<height / 3): 
		row = 1
	
	elif (y<height / 3 * 2): 
		row = 2
	
	elif(y<height): 
		row = 3
	
	else: 
		row = None
		
	# after getting the row and col, 
	# we need to draw the images at 
	# the desired positions 
	if(row and col and board[row-1][col-1] is None): 
		global XO 
		drawXO(row, col)
		return True

	return False
		
def reset_game(startup): 
	global board, winner, XO, draw
	XO = COMPUTER if random.randint(0, 1) == 0 else HUMAN
	draw = False
	game_initiating_window(startup)
	winner = None
	board = [[None]*3, [None]*3, [None]*3] 

#============================================================================
# My Stuff
#============================================================================
def main():
	startup = True
	while True:
		runGame(startup)
		startup = False

def runGame(startup):
	global XO
	reset_game(startup)

	while True: # main game loop
		draw_status() 
		if XO == COMPUTER:
			# Computer player's turn.
			getComputerMove()
			check_win()
			if winner or draw:
				break
			XO = HUMAN
		else:
			# Human player's turn.
			getHumanMove()
			check_win()
			if winner or draw:
				break
			XO = COMPUTER
			
	# Keep looping until player clicks the mouse or quits.
	while(True):
		draw_status() 
		pg.display.update() 
		CLOCK.tick(fps) 
		for event in pg.event.get(): 
			if event.type == QUIT: 
				pg.quit() 
				sys.exit() 
			elif event.type == MOUSEBUTTONDOWN: 
				return

def getComputerMove():
	global board
	
	board_array = np.reshape(board, (1, 9))[0].tolist()
	board_array = ['_' if x is None else x for x in board_array]

	game = TicTacToeGame(COMPUTER, HUMAN, board_array)
	move = computerPlayer.do_move(game)
	if move is not None:
		converter = [[1,1], [1,2], [1,3], [2,1], [2,2], [2,3], [3,1], [3,2], [3,3]]
		drawXO(converter[move][0], converter[move][1])
		board_array = [None if x == '_' else x for x in board_array]
		board = np.reshape(board_array, (3, 3)).tolist()

def getHumanMove():
	while True:
		for event in pg.event.get(): 
			if event.type == QUIT: 
				pg.quit() 
				sys.exit() 
			elif event.type == MOUSEBUTTONDOWN: 
				if user_click():
					return
	
if __name__ == '__main__':
    main()