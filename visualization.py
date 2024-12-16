import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

player = pygame.Rect((300, 250, 50, 50))

run = True

while run:
	screen.fill((0, 0, 0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()