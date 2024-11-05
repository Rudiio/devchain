import pygame
from game import Game
from game_board import GameBoard
from renderer import Renderer
from ui import UI

class Main:
    def __init__(self):
        pygame.init()
        self.running = True
        self.game_board = GameBoard()
        self.game = Game()
        self.game.game_board = self.game_board
        self.renderer = Renderer((300, 300), 'Arial', 20)
        self.renderer.game_board = self.game_board
        self.ui = UI(self)
        self.start_new_game()  # Initialize the game state

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle_events(event)
            self.renderer.clear_screen()
            self.renderer.draw_board()
            if self.game.check_game_over():
                winner = self.game_board.check_winner()
                if winner:
                    self.ui.update_status(f"Player {winner} wins!")
                else:
                    self.ui.update_status("It's a draw!")
                self.ui.new_game_button.draw(self.renderer)  # Draw the new game button
            else:
                self.ui.update_status(f"Player {self.game.game_board.get_current_turn()}'s turn")
            self.renderer.update_display()
            clock.tick(60)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Adjust the click position based on the actual screen size and game board size
                adjusted_pos = self.renderer.get_cell_from_position(event.pos)
                if self.game.check_game_over():
                    if self.ui.new_game_button.is_hovered(adjusted_pos):
                        self.ui.new_game_button.click()
                else:
                    self.ui.handle_click(adjusted_pos)

    def start_new_game(self):
        self.game.start_new_game()
        self.ui.update_status("New Game Started")

# Application entry point
if __name__ == '__main__':
    main_app = Main()
    main_app.run()
