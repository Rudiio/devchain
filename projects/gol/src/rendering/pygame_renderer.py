import pygame
from game.game import Game
from game.cell import Cell

class PygameRenderer:
    def __init__(self, cell_size: int, surface: pygame.Surface):
        self._cell_size = cell_size
        self._surface = surface

    def draw_grid(self, game: Game):
        for y in range(game.get_height()):
            for x in range(game.get_width()):
                rect = pygame.Rect(x * self._cell_size, y * self._cell_size,
                                   self._cell_size, self._cell_size)
                pygame.draw.rect(self._surface, pygame.Color(200, 200, 200), rect, 1)

    def draw_cell(self, cell: Cell, x: int, y: int):
        rect = pygame.Rect(x * self._cell_size, y * self._cell_size,
                           self._cell_size, self._cell_size)
        if cell.is_alive:  # Corrected from cell.is_alive() to cell.is_alive
            pygame.draw.rect(self._surface, pygame.Color(0, 0, 0), rect)
        else:
            pygame.draw.rect(self._surface, pygame.Color(200, 200, 200), rect)

    def render_cells(self, game: Game):
        for y in range(game.get_height()):
            for x in range(game.get_width()):
                cell = game.get_cell(x, y)
                self.draw_cell(cell, x, y)

    def update_display(self):
        pygame.display.flip()

    def handle_events(self, game: Game) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    grid_x = x // self._cell_size
                    grid_y = y // self._cell_size
                    game.toggle_cell_state(grid_x, grid_y)
                    self.render_cells(game)  # Update the display with the new state of the cells
                    self.update_display()  # Refresh the screen
        return True
