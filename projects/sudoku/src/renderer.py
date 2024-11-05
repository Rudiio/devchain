import pygame
import pygame.font

class Renderer:
    """
    Renderer class handles all rendering tasks using Pygame, including the game board, score, and end-game messages.
    """
    def __init__(self, screen_size=(500, 600), background_color=(250, 248, 239), grid_color=(187, 173, 160), empty_cell_color=(205, 193, 180), cell_colors=None, font_name='Arial', font_size=20):
        """
        Initialize the Renderer with the screen size, background color, grid color, cell colors, and font settings.
        """
        self.screen_size = screen_size
        self.background_color = background_color
        self.grid_color = grid_color
        self.empty_cell_color = empty_cell_color
        self.cell_colors = cell_colors or {
            2: (238, 228, 218), 
            4: (237, 224, 200),
            # Additional colors for higher numbers
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        self.font_name = font_name
        self.font_size = font_size
        self.screen = None
        self.font = None
        self.initialize_screen()

    def initialize_screen(self):
        """
        Initialize the Pygame display screen and font.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('2048 Game')
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def get_cell_color(self, value):
        """
        Get the color for a cell based on its value.
        """
        # Return the color for the value if it's in the predefined list
        return self.cell_colors.get(value, self.empty_cell_color)

    def render_grid(self, grid):
        """
        Render the game grid with cells and numbers.
        """
        self.screen.fill(self.background_color)
        cell_size = self.screen_size[0] // len(grid)
        border_size = 5  # Adding a border size for cell separation

        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                # Calculate the position and size of the cell
                cell_rect = pygame.Rect(
                    x * cell_size + border_size,
                    y * cell_size + border_size,
                    cell_size - 2 * border_size,
                    cell_size - 2 * border_size
                )
                # Get the color for the cell
                cell_color = self.get_cell_color(value)
                # Draw the cell
                pygame.draw.rect(self.screen, cell_color, cell_rect)
                # If the cell has a value, render the number
                if value:
                    text_surface = self.font.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(text_surface, text_rect)

    def render_score(self, score):
        """
        Render the current score on the screen.
        """
        score_surface = self.font.render(f'Score: {score}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(topright=(self.screen_size[0] - 20, 20))
        self.screen.blit(score_surface, score_rect)

    def render_end_game_message(self, message):
        """
        Render the end game message (win or lose) on the screen.
        """
        message_surface = self.font.render(message, True, (0, 0, 0))
        message_rect = message_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(message_surface, message_rect)

    def update_display(self):
        """
        Update the display with the rendered content.
        """
        pygame.display.flip()
