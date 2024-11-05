from utilities.direction import Direction
from entities.segment import Segment

class Snake:
    def __init__(self, initial_length, grid_size_x, grid_size_y):
        self._initial_length = initial_length
        self._grid_size_x = grid_size_x
        self._grid_size_y = grid_size_y
        self.reset()

    def move(self):
        head_x, head_y = self._body[0].get_position()
        if self._direction == Direction.UP:
            head_y -= 1
        elif self._direction == Direction.DOWN:
            head_y += 1
        elif self._direction == Direction.LEFT:
            head_x -= 1
        elif self._direction == Direction.RIGHT:
            head_x += 1
        
        last_segment_position = self._body[-1].get_position()

        for i in range(len(self._body) - 1, 0, -1):
            self._body[i].set_position(*self._body[i - 1].get_position())
        self._body[0].set_position(head_x, head_y)

        if self._growing:
            self._body.append(Segment(*last_segment_position))
            self._growing = False
            self._has_grown = True
        else:
            self._has_grown = False

    def grow(self):
        self._growing = True

    def check_collision(self, grid_size_x, grid_size_y):
        head_x, head_y = self.get_head_position()
        if head_x < 0 or head_x >= grid_size_x or head_y < 0 or head_y >= grid_size_y:
            return True
        for segment in self._body[1:]:
            if segment.get_position() == (head_x, head_y):
                return True
        return False

    def set_direction(self, new_direction):
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if new_direction != opposite_directions[self._direction] and new_direction != self._direction:
            self._direction = new_direction

    def get_head_position(self):
        return self._body[0].get_position()

    def get_body(self):
        return self._body

    def reset(self):
        center_x, center_y = self._grid_size_x // 2, self._grid_size_y // 2
        self._body = [Segment(center_x, center_y + i) for i in range(self._initial_length)]
        self._direction = Direction.UP
        self._growing = False
        self._has_grown = False
