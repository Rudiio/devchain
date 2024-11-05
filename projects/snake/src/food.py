import random
from segment import Segment

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0

    def spawn(self, snake_segments, screen_width, screen_height, segment_size):
        # Generate a random new position for the food
        # Ensure that the new position is not occupied by the snake
        # Align the food's position with the grid based on the segment size
        while True:
            self.x = random.randint(0, (screen_width // segment_size) - 1) * segment_size
            self.y = random.randint(0, (screen_height // segment_size) - 1) * segment_size
            if not any(segment.x == self.x and segment.y == self.y for segment in snake_segments):
                break

    def get_position(self):
        return self.x, self.y
