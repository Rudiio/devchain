import pygame
from utilities.direction import Direction
from entities.snake import Snake
from entities.food import Food

class Game:
    def __init__(self, grid_size_x, grid_size_y, cell_size):
        self.score = 0
        self.game_over = False
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.cell_size = cell_size
        self.snake = None
        self.food = Food(grid_size_x, grid_size_y)

    def start_game(self):
        self.snake = Snake(initial_length=3, grid_size_x=self.grid_size_x, grid_size_y=self.grid_size_y)
        self.food.spawn(self.snake.get_body())

    def end_game(self):
        self.game_over = True

    def update(self):
        self.snake.move()
        if self.snake.check_collision(self.grid_size_x, self.grid_size_y):
            self.end_game()
        head_position = self.snake.get_head_position()
        if head_position == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.get_body())
            self.increase_score(1)

    def render(self, screen):
        screen.fill((0, 0, 0))
        for segment in self.snake.get_body():
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment.get_position()[0] * self.cell_size, segment.get_position()[1] * self.cell_size, self.cell_size, self.cell_size))
        food_position = self.food.get_position()
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_position[0] * self.cell_size, food_position[1] * self.cell_size, self.cell_size, self.cell_size))
        self.render_score(screen)

    def handle_input(self, direction):
        self.snake.set_direction(direction)

    def increase_score(self, amount):
        self.score += amount

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def render_score(self, screen):
        font = pygame.font.SysFont(None, 36)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

def main():
    pygame.init()
    
    grid_size_x, grid_size_y = 20, 20
    cell_size = 20
    screen_width = grid_size_x * cell_size
    screen_height = grid_size_y * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Serpentine Feast')
    
    game = Game(grid_size_x, grid_size_y, cell_size)
    
    game.start_game()
    
    clock = pygame.time.Clock()
    
    running = True
    while running and not game.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.handle_input(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.handle_input(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.handle_input(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.handle_input(Direction.RIGHT)
        
        game.update()
        
        game.render(screen)
        
        pygame.display.flip()
        
        clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
