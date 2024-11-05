from segment import Segment

class Snake:
    def __init__(self, initial_length, speed):
        self.segments = [Segment(0, 0) for _ in range(initial_length)]
        self.direction = 'RIGHT'
        self.speed = speed

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        valid_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
        if new_direction in valid_directions and new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.get_head_position()
        if self.direction == 'UP':
            new_head = Segment(head_x, head_y - self.speed)
        elif self.direction == 'DOWN':
            new_head = Segment(head_x, head_y + self.speed)
        elif self.direction == 'LEFT':
            new_head = Segment(head_x - self.speed, head_y)
        elif self.direction == 'RIGHT':
            new_head = Segment(head_x + self.speed, head_y)
        self.segments.insert(0, new_head)
        self.segments.pop()

    def grow(self):
        tail = self.segments[-1]
        second_last_segment = self.segments[-2]
        # Determine the direction of the tail movement
        if tail.x == second_last_segment.x:  # Vertical movement
            if tail.y < second_last_segment.y:  # Moving down
                new_segment = Segment(tail.x, tail.y + self.speed)
            else:  # Moving up
                new_segment = Segment(tail.x, tail.y - self.speed)
        else:  # Horizontal movement
            if tail.x < second_last_segment.x:  # Moving right
                new_segment = Segment(tail.x + self.speed, tail.y)
            else:  # Moving left
                new_segment = Segment(tail.x - self.speed, tail.y)
        self.segments.append(new_segment)

    def check_collision(self):
        head_x, head_y = self.get_head_position()
        return any(segment.x == head_x and segment.y == head_y for segment in self.segments[1:])

    def get_head_position(self):
        return self.segments[0].x, self.segments[0].y

    def has_eaten_food(self, food_position):
        head_x, head_y = self.get_head_position()
        # Adjust the collision detection to account for the speed of the snake
        # and allow a range of positions where the snake can eat the food
        return (head_x + self.speed > food_position[0] and head_x < food_position[0] + self.speed and
                head_y + self.speed > food_position[1] and head_y < food_position[1] + self.speed)
