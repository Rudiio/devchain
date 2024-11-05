import pygame
import sys
from game import Game
from sound_manager import SoundManager

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.button_color = (0, 255, 0)
        self.bg_color = (0, 0, 0)
        self.sound_manager = SoundManager()  # Initialize SoundManager

    def display_start_screen(self):
        self.screen.fill(self.bg_color)
        title_surface = self.font.render('Snake Odyssey', True, (255, 255, 255))
        start_surface = self.small_font.render('Press Enter to Start', True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 100))
        self.screen.blit(start_surface, (self.screen.get_width() // 2 - start_surface.get_width() // 2, 300))
        pygame.display.flip()

    def update_score(self, score):
        score_surface = self.small_font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def show_game_over(self):
        game_over_surface = self.font.render('Game Over', True, (255, 0, 0))
        restart_surface = self.small_font.render('Press R to Restart', True, (255, 255, 255))
        self.screen.fill(self.bg_color)
        self.screen.blit(game_over_surface, (self.screen.get_width() // 2 - game_over_surface.get_width() // 2, 100))
        self.screen.blit(restart_surface, (self.screen.get_width() // 2 - restart_surface.get_width() // 2, 300))
        pygame.display.flip()
        self.sound_manager.play_game_over_sound()  # Play game over sound when showing game over screen

    def reset(self):
        self.screen.fill(self.bg_color)
        pygame.display.flip()
