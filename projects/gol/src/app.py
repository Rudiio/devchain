import pygame
from game.game import Game
from rendering.pygame_renderer import PygameRenderer

def main():
    width, height = 50, 30  # Predefined width and height for the game grid
    cell_size = 20  # Specified cell size for rendering

    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption('LifeCraft: The Cellular Automaton Explorer')

    renderer = PygameRenderer(cell_size, screen)  # Corrected instantiation with two arguments
    game = Game(width, height, renderer)
    
    game.start_stable_game()  # Initialize the grid with a stable pattern
    game.start_random_game()
    
    running = True
    while running:
        running = renderer.handle_events(game)  # Process user input events
        game.update()
        game.render()
        renderer.update_display()  # Update the screen with the rendered cells

        pygame.time.wait(100)  # Wait a little to see the changes on the screen

    pygame.quit()

if __name__ == "__main__":
    main()
