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
from games.tic_tac_toe import SimpleMiniMaxPlayer, TicTacToeGame
from games.game import DRAW
import os

# declaring the global variables 

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
MEDIA_PATH = f'{os.getcwd()}/examples/images/tictactoe'

# loading the images as python object 
initiating_window = pg.image.load(f"{MEDIA_PATH}/modified_cover.png") 
x_img = pg.image.load(f"{MEDIA_PATH}/X_modified.png") 
y_img = pg.image.load(f"{MEDIA_PATH}/o_modified.png") 

# resizing images 
initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

# for storing the 'x' or 'o' 
# value as character 
XO = None
HUMAN = 'o'
COMPUTER = 'x'
# 0 dummy, 10 super smart
DIFFICULTY = 10
computerPlayer = SimpleMiniMaxPlayer(COMPUTER, DIFFICULTY)
game = None
move2Point = [[1,1], [1,2], [1,3], [2,1], [2,2], [2,3], [3,1], [3,2], [3,3]]
point2Move = [ [0, 1, 2],
               [3, 4, 5],
			   [6, 7, 8]]

def get_point(move):
	row = move2Point[move][0]
	col = move2Point[move][1]
	return row, col

def get_move(row, col):
	return point2Move[row-1][col-1]

def is_game_over():
	if game.check_win(COMPUTER):
		return COMPUTER
	elif game.check_win(HUMAN):
		return HUMAN
	elif not game.is_moves_left():
		return DRAW
	else:
		return None

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
	
	outcome = is_game_over()
	
	if outcome is None: 
		message = "Computer's Turn" if XO == COMPUTER else "Human's Turn"
	elif outcome == DRAW:
		message = "Game Draw !"
	else: 
		message = "Computer won !" if XO == COMPUTER else "Human won !"
		
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
	
def drawXO(row, col):
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
		
	if(XO == COMPUTER): 
		
		# pasting x_img over the screen 
		# at a coordinate position of 
		# (pos_y, posx) defined in the 
		# above code 
		screen.blit(x_img, (posy, posx)) 
	
	else: 
		screen.blit(o_img, (posy, posx)) 

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
		
	return row, col

def draw_win(): 
	board = np.reshape(game.get_board(), (3, 3)).tolist()

	# checking for winning rows 
	for row in range(0, 3): 
		if((board[row][0] == board[row][1] == board[row][2]) and (board [row][0] is not None)): 
			pg.draw.line(screen, (250, 0, 0), 
						(0, (row + 1)*height / 3 -height / 6), 
						(width, (row + 1)*height / 3 - height / 6 ), 
						4) 
			break

	# checking for winning columns 
	for col in range(0, 3): 
		if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)): 
			pg.draw.line (screen, (250, 0, 0), ((col + 1)* width / 3 - width / 6, 0), \
						((col + 1)* width / 3 - width / 6, height), 4) 
			break

	# check for diagonal winners 
	if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None): 
		# game won diagonally left to right 
		pg.draw.line (screen, (250, 70, 70), (50, 50), (350, 350), 4) 
		
	if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None): 
		# game won diagonally right to left 
		pg.draw.line (screen, (250, 70, 70), (350, 50), (50, 350), 4) 
		
def reset_game(startup): 
	global XO, game
	XO = COMPUTER if random.randint(0, 1) == 0 else HUMAN
	game_initiating_window(startup)
	game = TicTacToeGame(COMPUTER, HUMAN)

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
			if is_game_over():
				draw_win()
				break
			XO = HUMAN
		else:
			# Human player's turn.
			getHumanMove()
			if is_game_over():
				draw_win()
				break
			XO = COMPUTER
			
	# Keep looping until player clicks the mouse or quits.
	while(True):
		draw_status() 
		for event in pg.event.get(): 
			if event.type == QUIT: 
				pg.quit() 
				sys.exit() 
			elif event.type == MOUSEBUTTONDOWN: 
				return

def getComputerMove():
	move = computerPlayer.do_move(game)
	if move is not None:
		row, col = get_point(move)
		drawXO(row, col)

def getHumanMove():
	while True:
		for event in pg.event.get(): 
			if event.type == QUIT: 
				pg.quit() 
				sys.exit() 
			elif event.type == MOUSEBUTTONDOWN: 
				row, col = user_click()
				try:
					move = get_move(row, col)
					game.do_move(move, HUMAN)
					drawXO(row, col)
					return
				except Exception as ex:
					print(f'Error : {ex}')
	
if __name__ == '__main__':
    main()