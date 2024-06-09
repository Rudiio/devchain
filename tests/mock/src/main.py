import pygame
import sys
from game_board import GameBoard
from game_manager import GameManager
from input_handler import InputHandler
from renderer import Renderer

class Main:
    def __init__(self):
        # Initialize Pygame and the clock for controlling the frame rate
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create instances of the GameManager, GameBoard, InputHandler, and Renderer
        self.game_manager = GameManager()
        self.game_board = GameBoard(self.game_manager)  # Pass the game_manager instance
        self.input_handler = InputHandler()
        self.renderer = Renderer()

    def main(self):
        # Initialize the game components
        self.game_board.initialize_grid()
        self.renderer.initialize_screen()
        self.game_loop()

    def game_loop(self):
        # Main game loop
        while not self.game_manager.is_game_over:
            self.handle_events()
            self.renderer.render_grid(self.game_board.grid)
            self.renderer.render_score(self.game_manager.score)
            pygame.display.update()
            self.clock.tick(60)  # Limit the game to 60 frames per second

            # Check win condition with the current grid
            if self.game_manager.check_win_condition(self.game_board.grid):
                self.renderer.render_end_game_message("Congratulations! You've won!")
                self.reset_or_quit()

            # Check if there are no valid moves left
            if not self.game_board.has_valid_moves():
                self.renderer.render_end_game_message("Game Over! No more valid moves.")
                self.reset_or_quit()

    def handle_events(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                direction = self.input_handler.get_direction(event)
                if direction:
                    # Ensure move_blocks returns a tuple (moved, merged_value)
                    moved, merged_value = self.game_board.move_blocks(direction)
                    if moved:
                        self.game_manager.update_score(merged_value)
                        self.game_board.add_new_number()

    def reset_or_quit(self):
        # Wait for user input to reset the game or quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_manager.reset_game()
                        self.game_board.initialize_grid()
                        self.game_loop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
