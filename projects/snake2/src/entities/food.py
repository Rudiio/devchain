import random

class Food:
    def __init__(self, grid_size_x, grid_size_y):
        self._x = 0
        self._y = 0
        self._grid_size_x = grid_size_x
        self._grid_size_y = grid_size_y
        self.spawn([])  # Spawn food at a random location initially

    def spawn(self, snake_body):
        occupied_positions = {segment.get_position() for segment in snake_body}
        while True:
            self._x = random.randint(0, self._grid_size_x - 1)
            self._y = random.randint(0, self._grid_size_y - 1)
            if (self._x, self._y) not in occupied_positions:
                break

    def get_position(self):
        return (self._x, self._y)

    def __str__(self):
        return f"Food position: ({self._x}, {self._y})"
