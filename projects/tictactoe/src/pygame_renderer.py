import pygame
import sys
from game import Game
from symbol import Symbol
from game_status import GameStatus

class PygameRenderer:
    def __init__(self, game):
        self._game = game
        # Initialize Pygame and set up the display
        pygame.init()
        self._screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Tic-Tac-Toe Triumph')

    def draw_grid(self):
        # Set the color for the grid lines
        line_color = (0, 0, 0)
        # Draw the vertical grid lines
        pygame.draw.line(self._screen, line_color, (100, 0), (100, 300), 2)
        pygame.draw.line(self._screen, line_color, (200, 0), (200, 300), 2)
        # Draw the horizontal grid lines
        pygame.draw.line(self._screen, line_color, (0, 100), (300, 100), 2)
        pygame.draw.line(self._screen, line_color, (0, 200), (300, 200), 2)

    def render(self):
        # Clear the screen
        self._screen.fill((255, 255, 255))
        # Draw the game board grid
        self.draw_grid()
        # Draw the symbols
        for row in range(3):
            for col in range(3):
                symbol = self._game.get_symbol_at(row, col)
                if symbol != Symbol.EMPTY:
                    self.draw_symbol(row, col, symbol)
        # Check if the game has ended and display the game end message if it has
        if self._game.get_game_status() != GameStatus.IN_PROGRESS:
            self.display_game_end_message()
        # Update the display
        pygame.display.flip()

    def draw_symbol(self, row, col, symbol):
        # Define the center position based on row and col
        center_x = col * 100 + 50
        center_y = row * 100 + 50
        # Define colors for symbols
        color_x = (0, 0, 255)  # Blue color for X
        color_o = (255, 0, 0)  # Red color for O
        if symbol == Symbol.X:
            # Draw X symbol in blue
            pygame.draw.line(self._screen, color_x, (center_x - 20, center_y - 20), (center_x + 20, center_y + 20), 3)
            pygame.draw.line(self._screen, color_x, (center_x + 20, center_y - 20), (center_x - 20, center_y + 20), 3)
        elif symbol == Symbol.O:
            # Draw O symbol in red
            pygame.draw.circle(self._screen, color_o, (center_x, center_y), 20, 3)

    def display_game_end_message(self):
        # Define the font and message based on the game status
        font = pygame.font.Font(None, 36)
        game_status = self._game.get_game_status()
        if game_status == GameStatus.X_WON:
            message = "X Won!"
        elif game_status == GameStatus.O_WON:
            message = "O Won!"
        elif game_status == GameStatus.DRAW:
            message = "It's a Draw!"
        # Render the message
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(150, 150))
        self._screen.blit(text, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the game is in progress before allowing a move to be made
                if self._game.get_game_status() == GameStatus.IN_PROGRESS:
                    # Convert mouse position to row and col
                    x, y = pygame.mouse.get_pos()
                    row = y // 100
                    col = x // 100
                    # Check if the selected cell is empty before making a move
                    if self._game.get_symbol_at(row, col) == Symbol.EMPTY:
                        self._game.make_move(row, col)
                        self.render()  # Updated to call render directly
