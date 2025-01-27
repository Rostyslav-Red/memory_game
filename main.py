import pygame
from constants import *
from game import Game
from visualization import draw_board
from csv import writer
import os
import time

# time.sleep(5)


def pygame_init():
    pygame.init()
    pygame.font.init()
    game_font = pygame.font.Font(font_path, 36)
    game_screen = pygame.display.set_mode((window_height, window_width))
    pygame.display.set_caption("Memory Game")
    if has_music:
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play()
    return game_screen, game_font


def determine_elements_sizes():
    n_rows = n_cols = game.board.size
    _tile_size = min((window_width - padding * (n_cols + 1)) // n_cols,
                    (window_height - top_spacing - padding * (n_rows + 1)) // n_rows)
    _margin_x = (window_width - (n_cols * _tile_size + padding * (n_cols - 1))) // 2
    _margin_y = top_spacing + (window_height - top_spacing - (n_rows * _tile_size + padding * (n_rows - 1))) // 2
    return n_rows, n_cols, _tile_size, _margin_x, _margin_y


# Initialize the main values for the game
screen, font = pygame_init()
game = Game(size=3, filled_number=3)

# Main Game Loop
run = True
start_time = pygame.time.get_ticks()
level_transition_start = None

# data file
if os.listdir("./data"):
    file_name = "data_" + str(int(max(os.listdir("./data"))[5:-4])+1) + ".csv"
else:
    file_name = "data_1.csv"
file = open(f"./data/{file_name}", "w", newline="")
writer = writer(file)
writer.writerow(["x_coord", "y_coord", "level", "board_size", "is_correct",
                 "lives", "time", "has_music", "participant_id"])

while run:
    # Calculate dynamic sizes and margins
    rows, cols, tile_size, margin_x, margin_y = determine_elements_sizes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            file.close()

        match game.phase:
            case "break_phase":
                if pygame.time.get_ticks() - start_time > break_time:
                    game.phase = "memorize_phase"
                    start_time = pygame.time.get_ticks()
            case "memorize_phase":
                if pygame.time.get_ticks() - start_time > memorize_time:
                    game.phase = "playing_phase"
                    for row in game.board.board:
                        for cell in row:
                            cell.is_discovered = False  # Hide the correct tiles after memorization time
            case "playing_phase":
                # Player clicked on a screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for row in game.board.board:
                        for cell in row:
                            # pygame.quit()
                            rect = pygame.Rect(
                                margin_x + cell.y * (tile_size + padding), margin_y + cell.x * (tile_size + padding), tile_size,
                                tile_size)
                            if rect.collidepoint(pos) and not cell.is_discovered:
                                cell.is_discovered = True
                                if not cell.is_filled:
                                    if not game.lose_life():
                                        # game.reset_game()  # Reset game on game over
                                        writer.writerow([cell.x, cell.y, game.level, game.board.size, cell.is_filled,
                                                         game.lives, pygame.time.get_ticks(),
                                                         has_music, participant_id])
                                        file.close()
                                        run = False
                                        break
                                writer.writerow([cell.x, cell.y, game.level, game.board.size, cell.is_filled,
                                                 game.lives, pygame.time.get_ticks(), has_music, participant_id])

                                break
                # Advance level
                if game.board.find_correctly_guessed_cells_number() == game.board.filled_number:
                    game.phase = "level_transition_phase"
                    level_transition_start = pygame.time.get_ticks()
                    game.advance_level()
            case "level_transition_phase":
                if pygame.time.get_ticks() - level_transition_start > transition_time:
                    game.phase = "break_phase"
                    start_time = pygame.time.get_ticks()

    draw_board(tile_size, margin_x, margin_y, screen, font, game)
    pygame.display.flip()
