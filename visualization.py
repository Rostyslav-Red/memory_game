import pygame
from board import Board

# Variables setup
board = Board(5, 4)  # Test board
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
window_height = 700
window_width = 700
tiles = []
tile_size = 80
memorize_time = 2000 #time given to memorize at the start (in milliseconds)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((window_height, window_width))
pygame.display.set_caption("Memory Game")

# Tile initialization
for row in range(board.size):
	for column in range(board.size):
		rect = pygame.Rect(100 * (column + 1), 100 * (row + 1), tile_size, tile_size)
		if board.board[row][column].is_filled:
			color = green
		else:
			color = red
		tiles.append({"rect": rect, "color": color, "is_filled": board.board[row][column].is_filled})

# Pre-Game (Shows tiles' real colors to remember them)
start_time = pygame.time.get_ticks()
screen.fill(black)
for tile in tiles:
	pygame.draw.rect(screen, tile["color"], tile["rect"])
pygame.display.flip()
for tile in tiles:
	tile["color"] = blue

# Main game loop
run = True
while run:
	if pygame.time.get_ticks() - start_time > memorize_time:	
		for tile in tiles:
			pygame.draw.rect(screen, tile["color"], tile["rect"])

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				for tile in tiles:
					if tile["rect"].collidepoint(event.pos):  # Check if the tile was clicked
						if tile["is_filled"]:
							tile["color"] = green  # Change color to green if correct
						else:
							tile["color"] = red # Change color to red if incorrect (should be replaced by losing lives later)
	else:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pass #Blocking mouse input during memorization phase
	pygame.display.flip()
pygame.quit()