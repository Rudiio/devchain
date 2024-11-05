import pygame

class Renderer:
    """
    Renderer class is responsible for all rendering operations in the game, such as drawing the paddles,
    the ball, the score, and the game over message. It also handles screen updates and clearing.
    """
    def __init__(self, screen_size, game_area_rect, font_name, font_size):
        """
        Initializes the Renderer with the given screen size, game area rectangle, font name, and font size.
        
        :param screen_size: Tuple of (width, height) for the screen dimensions.
        :param game_area_rect: pygame.Rect defining the game area boundaries.
        :param font_name: String name of the font to use.
        :param font_size: Integer size of the font.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.font = pygame.font.Font(font_name, font_size)
        self.game_area_rect = game_area_rect

    def draw_paddle(self, paddle):
        """
        Draws the paddle on the screen.
        
        :param paddle: Paddle object to be drawn.
        """
        pygame.draw.rect(self.screen, pygame.Color('white'), paddle.get_rect())

    def draw_ball(self, ball):
        """
        Draws the ball on the screen.
        
        :param ball: Ball object to be drawn.
        """
        pygame.draw.circle(self.screen, pygame.Color('white'), (ball.x, ball.y), ball.radius)

    def draw_score(self, player_score, ai_score):
        """
        Draws the current score of the player and the AI on the screen.
        
        :param player_score: Integer score of the player.
        :param ai_score: Integer score of the AI.
        """
        player_score_text = self.font.render(f"Player: {player_score}", True, pygame.Color('white'))
        ai_score_text = self.font.render(f"AI: {ai_score}", True, pygame.Color('white'))
        self.screen.blit(player_score_text, (50, 20))
        self.screen.blit(ai_score_text, (self.screen.get_width() - 150, 20))

    def draw_game_over(self, winner):
        """
        Draws the game over message on the screen.
        
        :param winner: String indicating the winner ("player" or "AI").
        """
        if winner == "player":
            message = "You Win!"
        else:
            message = "You Lose!"
        game_over_text = self.font.render(message, True, pygame.Color('white'))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(game_over_text, text_rect)

    def clear_screen(self):
        """
        Clears the screen to prepare for the next frame.
        """
        self.screen.fill(pygame.Color('black'))

    def update_display(self):
        """
        Updates the display to show the new frame.
        """
        pygame.display.flip()
