import pygame
import sys
from ui import UI
from game import Game
from sound_manager import SoundManager

def handle_restart(ui):
    # Reset the game state
    ui.reset()  # Clear the screen and reset UI elements

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Odyssey')

    # Create instances of UI and SoundManager
    ui = UI(screen)
    sound_manager = SoundManager()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start Game on Enter key
                    game = Game(ui, sound_manager)
                    game.run()
                elif event.key == pygame.K_r:  # Restart Game on 'R' key
                    handle_restart(ui)

        # Display the start screen
        ui.display_start_screen()

        # Update the display
        pygame.display.flip()

    # Clean exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
