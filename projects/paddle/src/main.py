import pygame
from game import Game
from renderer import Renderer

class Main:
    """
    Main class is the entry point of the application. It initializes the game, manages the game loop,
    processes events, updates the game state, and delegates rendering to the Renderer class.
    """
    def __init__(self):
        """
        Initializes the Main class, setting up the game, renderer, and clock.
        """
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.game = Game(max_score=10)
        screen_size = (800, 600)
        game_area_rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.renderer = Renderer(screen_size, game_area_rect, None, 30)
        self.game.initialize_game_elements(
            screen_width=screen_size[0],
            screen_height=screen_size[1],
            paddle_width=20,
            paddle_height=100,
            ball_radius=10,
            paddle_speed=5,
            ball_speed=5,
            ai_difficulty=2
        )

    def main_loop(self):
        """
        The main game loop that keeps the game running until the user quits or the game ends.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Run the game at 60 frames per second

    def handle_events(self):
        """
        Handles events such as keyboard inputs and quitting the game.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.game.move_player_paddle_up()
        if keys[pygame.K_DOWN]:
            self.game.move_player_paddle_down()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        Updates the game state, including the positions of the ball and paddles, and checks the score.
        """
        self.game.update()
        if self.game.is_game_over():
            self.running = False

    def render(self):
        """
        Renders the game state to the screen, including the paddles, ball, and score.
        """
        self.renderer.clear_screen()
        self.renderer.draw_paddle(self.game.player_paddle)
        self.renderer.draw_paddle(self.game.ai_paddle)
        self.renderer.draw_ball(self.game.ball)
        player_score, ai_score = self.game.get_scores()
        self.renderer.draw_score(player_score, ai_score)
        if self.game.is_game_over():
            winner = "player" if player_score > ai_score else "AI"
            self.renderer.draw_game_over(winner)
        self.renderer.update_display()

# Code to run the application
if __name__ == "__main__":
    main = Main()
    main.main_loop()
    pygame.quit()
