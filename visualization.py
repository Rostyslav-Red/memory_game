import pygame
from board import Board
from game import Game

# Variables setup
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
window_height = 900
window_width = 900
tiles = []
tile_size = 80
memorize_time = 2000 #time given to memorize at the start (in milliseconds)
transition_time = 1500
padding = 10
top_spacing = 100
font_path = "Nunito-Regular.ttf"

# Pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.Font(font_path, 36)
screen = pygame.display.set_mode((window_height, window_width))
pygame.display.set_caption("Memory Game")

# Initialize Game
game = Game(size=3, filled_number=3)


def draw_board(tile_size, margin_x, margin_y, memorize_phase, level_transition_phase):
    screen.fill(black)
    lives_text = font.render(f"Lives: {game.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    level_text = font.render(f"Level: {game.level}", True, (255, 255, 255))
    level_rect = level_text.get_rect(topright=(window_width - 10, 10))
    screen.blit(level_text, level_rect)


    for row in game.board.board:
        for cell in row:
            if memorize_phase:
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
    if level_transition_phase:
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))

        # Display "Level Complete!" message
        message_text = font.render("Level Complete!", True, (255, 255, 255))
        text_rect = message_text.get_rect(center=(window_width // 2, window_height // 2))
        screen.blit(message_text, text_rect)


# Main Game Loop
run = True
memorize_phase = True
level_transition_phase = False
start_time = pygame.time.get_ticks()
level_transition_start = None

while run:
    # Calculate dynamic sizes and margins
    rows, cols = game.board.size, game.board.size
    tile_size = min((window_width - padding * (cols + 1)) // cols, (window_height - top_spacing - padding * (rows + 1)) // rows)
    margin_x = (window_width - (cols * tile_size + padding * (cols - 1))) // 2
    margin_y = top_spacing + (window_height - top_spacing - (rows * tile_size + padding * (rows - 1))) // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Disable clicks during memorization phase
        if not (memorize_phase or level_transition_phase) and event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for row in game.board.board:
                for cell in row:
                    rect = pygame.Rect( 
                        margin_x + cell.y * (tile_size + padding), margin_y + cell.x * (tile_size + padding), tile_size, tile_size)
                    if rect.collidepoint(pos) and not cell.is_discovered:
                        cell.is_discovered = True
                        if not cell.is_filled:
                            if not game.lose_life():
                                game.reset_game()  # Reset game on game over
                        break

    if memorize_phase:
        if pygame.time.get_ticks() - start_time > memorize_time:
            memorize_phase = False
            for row in game.board.board:
                for cell in row:
                    cell.is_discovered = False  # Hide the correct tiles after memorization time

    if level_transition_phase:
        if pygame.time.get_ticks() - level_transition_start > transition_time:
            level_transition_phase = False
            memorize_phase = True
            start_time = pygame.time.get_ticks()

    # Advance level
    if not level_transition_phase and game.board.find_correctly_guessed_cells_number() == game.board.filled_number:
        level_transition_phase = True
        level_transition_start = pygame.time.get_ticks()
        game.advance_level()
        
    draw_board(tile_size, margin_x, margin_y, memorize_phase, level_transition_phase)
    pygame.display.flip()