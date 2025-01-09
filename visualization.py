import pygame
from board import Board
from game import Game
from constants import *

# from main import pygame_init
# screen, font = pygame_init()
#
# # Initialize Game
# game = Game(size=3, filled_number=3)


def draw_board(tile_size, margin_x, margin_y, screen, font, game):
    screen.fill(black)
    lives_text = font.render(f"Lives: {game.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    level_text = font.render(f"Level: {game.level}", True, (255, 255, 255))
    level_rect = level_text.get_rect(topright=(window_width - 10, 10))
    screen.blit(level_text, level_rect)


    for row in game.board.board:
        for cell in row:
            if game.phase == "memorize_phase":
                # During memorization phase, show the actual tile color
                if cell.is_filled:
                    color = green 
                else:
                    color = red 
            else:
                # After memorization phase, hide tiles
                if cell.is_discovered:
                    if cell.is_filled:
                        color = green
                    else:
                        color = red
                else:
                    color = blue
            rect = pygame.Rect(margin_x + cell.y * (tile_size + padding), margin_y + cell.x * (tile_size + padding), tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)

    # Render transition overlay and message
    if game.phase == "level_transition_phase":
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))

        # Display "Level Complete!" message
        message_text = font.render("Level Complete!", True, (255, 255, 255))
        text_rect = message_text.get_rect(center=(window_width // 2, window_height // 2))
        screen.blit(message_text, text_rect)


