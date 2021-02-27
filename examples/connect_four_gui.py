#=====================================================================
# Play with:
# https://www.helpfulgames.com/subjects/brain-training/connect-four.html
#=====================================================================
from games.connect_four import ConnectFourGame, MiniMaxPlayer, DRAW, AI_PIECE, PLAYER_PIECE

import random
import pygame
from pygame.locals import *
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0, 200, 0 )
LABEL_COLOR = GREEN

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

PLAYER = 0
AI = 1
DIFFICULTY = 3

PLAYER_COLOR = {PLAYER_PIECE: YELLOW, AI_PIECE: RED}

computerPlayer = MiniMaxPlayer(AI_PIECE, DIFFICULTY)
game = None
turn = None

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.update()

myfont = pygame.font.SysFont("Arial", 48)

def draw_board(game):
    board = game.get_board()    
    for c in range(game.get_cols()):
        for r in range(game.get_rows()):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
    for c in range(game.get_cols()):
        for r in range(game.get_rows()):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, PLAYER_COLOR[PLAYER_PIECE], (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, PLAYER_COLOR[AI_PIECE], (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def reset_game(): 
    global turn, game
    turn = random.randint(PLAYER, AI)
    #turn = PLAYER
    #turn = AI
    game = ConnectFourGame(AI_PIECE, PLAYER_PIECE, ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

def getComputerMove():
    label = myfont.render("Please wait...", 1, LABEL_COLOR)
    screen.blit(label, (40,10))
    pygame.display.update()
    computerPlayer.do_move(game)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    pygame.display.update()

def getHumanMove():
    while True:
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame.quit() 
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, PLAYER_COLOR[PLAYER_PIECE], (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            elif event.type == MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                try:
                    game.do_move(col, PLAYER_PIECE)
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    return
                except Exception as ex:
                    print(f'Error : {ex}')

def is_game_over():
	if game.check_win(AI_PIECE):
		return AI_PIECE
	elif game.check_win(PLAYER_PIECE):
		return PLAYER_PIECE
	elif not game.is_moves_left():
		return DRAW
	else:
		return None

def draw_win():
    winner = is_game_over()
    if winner is None:
        return

    if winner == DRAW:
        label = myfont.render("Draw !!", 1, LABEL_COLOR)
    else:
        text = 'Human' if winner == PLAYER_PIECE else 'Computer'
        label = myfont.render(f"{text} wins!!", 1, LABEL_COLOR)

    screen.blit(label, (40,10))

def main():
	while True:
		runGame()

def runGame():
    global turn
    reset_game()

    while True: # main game loop
        draw_board(game) 
        #print(game.to_string())
        if turn == AI:
            # Computer player's turn.
            getComputerMove()
            if is_game_over():
                draw_win()
                break
            turn = PLAYER
        else:
            # Human player's turn.
            getHumanMove()
            if is_game_over():
                draw_win()
                break
            turn = AI
    
    # Keep looping until player clicks the mouse or quits.
    while(True):
        draw_board(game) 
        #print(game.to_string()) 
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame.quit() 
                sys.exit() 
            elif event.type == MOUSEBUTTONDOWN: 
                return

if __name__ == '__main__':
    main()
