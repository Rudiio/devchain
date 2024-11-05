import pygame
from snake import Snake
from food import Food

class GameApp:
    def __init__(self, width, height):
        self.score = 0
        self.screen_width = width
        self.screen_height = height
        self.game_over = False
        self.snake = Snake(initial_length=5, speed=5)
        self.food = Food()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.food.spawn(self.snake.segments, self.screen_width, self.screen_height, 10)  # Added segment_size argument
        self.font_small = pygame.font.SysFont(None, 35)
        self.font_large = pygame.font.SysFont(None, 55)

    def run(self):
        clock = pygame.time.Clock()
        try:
            while not self.game_over:
                self.handle_events()
                self.update_game_state()
                self.render()
                clock.tick(30)  # Increase the game's frame rate to make the snake's movements faster
        except KeyboardInterrupt:
            self.end_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.change_direction('RIGHT')

    def update_game_state(self):
        self.snake.move()
        if self.snake.check_collision() or not (0 <= self.snake.get_head_position()[0] < self.screen_width and
                                                0 <= self.snake.get_head_position()[1] < self.screen_height):
            self.end_game()
        elif self.snake.has_eaten_food(self.food.get_position()):
            self.snake.grow()
            self.food.spawn(self.snake.segments, self.screen_width, self.screen_height, 10)  # Added segment_size argument
            self.score += 1

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        for segment in self.snake.segments:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment.x, segment.y, 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, 10, 10))
        
        # Render the score
        score_text = self.font_small.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))  # Position the score in the top-left corner
        
        pygame.display.flip()  # Update the full display Surface to the screen

    def end_game(self):
        self.game_over = True
        # Display the 'Game Over' message
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        game_over_text = self.font_large.render('Game Over!', True, (255, 255, 255))
        score_text = self.font_large.render(f'Your score was: {self.score}', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        score_rect = score_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()  # Update the full display Surface to the screen
        pygame.time.wait(3000)  # Wait for 3 seconds before closing the game
