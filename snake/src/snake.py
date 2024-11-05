# snake.py
import pygame

class Snake:
    def __init__(self):
        self.position = [(100, 100), (90, 100), (80, 100)]  # Initial position of the snake
        self.length = 3  # Initial length of the snake
        self.direction = (10, 0)  # Initial direction (moving right)

    def move(self):
        head_x, head_y = self.position[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.position.insert(0, new_head)  # Add new head position
        if len(self.position) > self.length:
            self.position.pop()  # Remove the last segment if the snake hasn't grown

    def grow(self):
        self.length += 1  # Increase the length of the snake

    def collide_with_self(self):
        head = self.position[0]
        return head in self.position[1:]  # Check if the head collides with any body segment

    def change_direction(self, x, y):
        if (x, y) != (-self.direction[0], -self.direction[1]):  # Prevent reversing direction
            self.direction = (x * 10, y * 10)  # Update direction with speed factor

    def reset(self):
        self.__init__()  # Reset the snake to its initial state
