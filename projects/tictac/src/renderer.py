import pygame

class Renderer:
    def __init__(self, screen_size, font_name, font_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.font = pygame.font.SysFont(font_name, font_size)
        self.game_board = None  # This will be set by the Main class

    def draw_board(self):
        if not self.game_board:
            raise ValueError("GameBoard not set in Renderer")

        self.screen.fill((255, 255, 255))  # Fill the screen with a white background

        # Draw the Tic-Tac-Toe grid
        color = (0, 0, 0)  # Black color for the grid lines
        board_height = self.screen.get_height()
        board_width = self.screen.get_width()
        cell_size = board_height // 3

        for i in range(1, 3):
            pygame.draw.line(self.screen, color, (i * cell_size, 0), (i * cell_size, board_height), 5)
            pygame.draw.line(self.screen, color, (0, i * cell_size), (board_width, i * cell_size), 5)

        # Draw the X's and O's
        for y in range(3):
            for x in range(3):
                symbol = self.game_board.board[y][x]
                if symbol:
                    self.animate_symbol((x, y), symbol)

    def draw_status(self, message):
        # Render the status message and blit it onto the screen
        text_surface = self.font.render(message, True, (0, 0, 0))
        rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 30))
        self.screen.blit(text_surface, rect)

    def animate_symbol(self, position, symbol):
        # Animate the symbol placement
        cell_size = self.screen.get_height() // 3
        x, y = position
        center_x, center_y = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)

        if symbol == 'X':
            offset = cell_size // 4
            pygame.draw.line(self.screen, (255, 0, 0), (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 10)
            pygame.draw.line(self.screen, (255, 0, 0), (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 10)
        elif symbol == 'O':
            pygame.draw.circle(self.screen, (0, 0, 255), (center_x, center_y), cell_size // 4, 10)

    def clear_screen(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))

    def update_display(self):
        # Update the display
        pygame.display.flip()

    def get_cell_from_position(self, position):
        # Translate a pixel position on the screen to a cell position on the game board
        cell_size = self.screen.get_height() // 3
        x, y = position
        col = x // cell_size
        row = y // cell_size
        # Ensure that the cell coordinates are within the valid range
        col = max(0, min(col, 2))
        row = max(0, min(row, 2))
        return (row, col)
