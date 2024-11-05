# game.py

import pygame
from snake import Snake
from food import Food

class Game:
    def __init__(self, ui, sound_manager):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.ui = ui
        self.sound_manager = sound_manager

    def run(self):
        while not self.game_over:
            self.handle_input()
            self.snake.move()
            self.check_collisions()
            if self.snake.eat_food(self.food):
                self.score += 1
                self.food.generate_new_food()
                self.snake.grow()
                self.sound_manager.play_eat_sound()  # Play eat sound
            self.ui.update_score(self.score)
            self.ui.render()
            pygame.display.flip()
            pygame.time.delay(100)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(1, 0)

    def check_collisions(self):
        if self.snake.collide_with_wall() or self.snake.collide_with_self():
            self.game_over = True
            self.sound_manager.play_game_over_sound()  # Play game over sound
            self.ui.show_game_over()

    def reset_game(self):
        self.snake.reset()
        self.food.generate_new_food()
        self.score = 0
        self.game_over = False
        self.ui.reset()
