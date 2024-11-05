import random
from game.cell import Cell

class Game:
    def __init__(self, width: int, height: int, renderer):
        self._width = width
        self._height = height
        self._grid = [[Cell(False) for _ in range(width)] for _ in range(height)]
        self._renderer = renderer

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def start_new_game(self):
        self._grid = [[Cell(False) for _ in range(self._width)] for _ in range(self._height)]

    def start_random_game(self):
        self._grid = [[Cell(random.choice([True, False])) for _ in range(self._width)] for _ in range(self._height)]

    def start_stable_game(self):
        # Initialize the grid with all dead cells
        self._grid = [[Cell(False) for _ in range(self._width)] for _ in range(self._height)]
        # Define a stable pattern such as a 'block'
        stable_pattern = [
            (1, 1), (1, 2),
            (2, 1), (2, 2)
        ]
        # Place the stable pattern in the center of the grid
        offset_x = self._width // 2 - 1
        offset_y = self._height // 2 - 1
        for x, y in stable_pattern:
            self._grid[y + offset_y][x + offset_x].set_is_alive(True)

    def update(self):
        new_grid = [[Cell(False) for _ in range(self._width)] for _ in range(self._height)]
        for y in range(self._height):
            for x in range(self._width):
                alive_neighbors = self._count_alive_neighbors(x, y)
                cell = self._grid[y][x]
                if cell.is_alive:  # Fixed the method call to property access
                    # A live cell with two or three live neighbors stays alive
                    if alive_neighbors == 2 or alive_neighbors == 3:
                        new_grid[y][x].set_is_alive(True)
                else:
                    # A dead cell with exactly three live neighbors becomes alive
                    if alive_neighbors == 3:
                        new_grid[y][x].set_is_alive(True)
        self._grid = new_grid

    def render(self):
        self._renderer.draw_grid(self)
        for y in range(self._height):
            for x in range(self._width):
                cell = self._grid[y][x]
                self._renderer.draw_cell(cell, x, y)

    def toggle_cell_state(self, x: int, y: int):
        if 0 <= x < self._width and 0 <= y < self._height:
            self._grid[y][x].toggle_state()

    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._grid[y][x]
        else:
            raise IndexError("Cell position out of bounds")

    def _count_alive_neighbors(self, x: int, y: int) -> int:
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (dx != 0 or dy != 0) and 0 <= nx < self._width and 0 <= ny < self._height:
                    if self._grid[ny][nx].is_alive:  # Fixed the method call to property access
                        count += 1
        return count
