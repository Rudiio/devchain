import pygame
from game_app import GameApp

# Initialize pygame
pygame.init()

# Set up the game entry point
if __name__ == '__main__':
    # Define screen dimensions
    screen_width = 640
    screen_height = 480

    # Create an instance of the GameApp
    game_app = GameApp(screen_width, screen_height)

    # Start the game loop
    game_app.run()

# Quit pygame
pygame.quit()
