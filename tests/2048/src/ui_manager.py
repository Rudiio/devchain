import pygame
import sys

class UIManager:
    def __init__(self, game_board, score_manager, size=4, tile_size=100, tile_margin=20):
        self.game_board = game_board
        self.score_manager = score_manager
        self.size = size
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.window_size = self.calculate_window_size()
        self.font = None
        self.message_start_time = None
        self.message_duration = 2000  # Duration to show the message in milliseconds
        self.current_message = None
        self.init_pygame()

    def calculate_window_size(self):
        return ((self.tile_size + self.tile_margin) * self.size + self.tile_margin,
                (self.tile_size + self.tile_margin) * self.size + self.tile_margin + 60)

    def init_pygame(self):
        # Removed the redundant pygame.init() call
        self.font = pygame.font.SysFont("Arial", 24)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('MergeMaster 2048')

    def draw_board(self):
        self.screen.fill((187, 173, 160))
        for x in range(self.size):
            for y in range(self.size):
                value = self.game_board.get_tile(x, y)
                tile_color = self.get_tile_color(value)
                rect = (x * (self.tile_size + self.tile_margin) + self.tile_margin,
                        y * (self.tile_size + self.tile_margin) + self.tile_margin,
                        self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, tile_color, rect)
                if value:
                    text_surface = self.font.render(str(value), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))
                    self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def get_tile_color(self, value):
        colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            # Add more colors for higher value tiles if needed
        }
        return colors.get(value, (205, 193, 180))  # Default color for unknown values

    def display_score(self):
        score = self.score_manager.get_score()
        text_surface = self.font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(text_surface, (self.tile_margin, self.window_size[1] - 40))

    def show_message(self, message):
        self.current_message = message
        self.message_start_time = pygame.time.get_ticks()

    def draw_message(self):
        if self.current_message and self.message_start_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.message_start_time < self.message_duration:
                text_surface = self.font.render(self.current_message, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.window_size[0] / 2, self.window_size[1] / 2))
                pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(200, 50))
                self.screen.blit(text_surface, text_rect)
                pygame.display.update()
            else:
                self.current_message = None
                self.message_start_time = None

    def update_ui(self):
        self.draw_board()
        self.display_score()
        self.draw_message()
        pygame.display.update()

# Example usage:
# Assuming we have a game_board instance of GameBoard and a score_manager instance of ScoreManager
# ui_manager = UIManager(game_board, score_manager)
# ui_manager.update_ui()
# ui_manager.show_message("You Win!")
