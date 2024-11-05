import random

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self.generate_new_position()

    def generate_new_position(self):
        x = random.randint(0, (self.width // 10) - 1) * 10
        y = random.randint(0, (self.height // 10) - 1) * 10
        return (x, y)

    def check_collision(self, snake_head):
        return self.position == snake_head

    def get_position(self):
        return self.position

    def reset_food(self):
        self.position = self.generate_new_position()
