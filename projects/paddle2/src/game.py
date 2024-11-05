import pygame
from paddle import Paddle
from ball import Ball
from ai import AI

class Game:
    """
    Game class manages the game state, including initializing game elements, updating positions
    of the ball and paddles, keeping score, checking for win/loss conditions, and resetting
    the game when necessary.
    """
    def __init__(self, max_score):
        """
        Initializes a new Game object with a maximum score.

        :param max_score: The score at which the game will end.
        """
        self.player_score = 0
        self.ai_score = 0
        self.max_score = max_score
        self.player_paddle = None
        self.ai_paddle = None
        self.ball = None
        self.ai = None
        self.screen_width = None
        self.screen_height = None

    def initialize_game_elements(self, screen_width, screen_height, paddle_width, paddle_height,
                                 ball_radius, paddle_speed, ball_speed, ai_difficulty):
        """
        Initializes the game elements including paddles, ball, and AI.

        :param screen_width: The width of the game screen.
        :param screen_height: The height of the game screen.
        :param paddle_width: The width of the paddles.
        :param paddle_height: The height of the paddles.
        :param ball_radius: The radius of the ball.
        :param paddle_speed: The movement speed of the paddles.
        :param ball_speed: The movement speed of the ball.
        :param ai_difficulty: The difficulty level of the AI opponent.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        boundary_top = 0
        boundary_bottom = screen_height

        # Initialize player paddle
        self.player_paddle = Paddle(
            x=50,
            y=screen_height // 2 - paddle_height // 2,
            speed=paddle_speed,
            height=paddle_height,
            width=paddle_width,
            boundary_top=boundary_top,
            boundary_bottom=boundary_bottom
        )

        # Initialize AI paddle
        self.ai_paddle = Paddle(
            x=screen_width - 50 - paddle_width,
            y=screen_height // 2 - paddle_height // 2,
            speed=paddle_speed,
            height=paddle_height,
            width=paddle_width,
            boundary_top=boundary_top,
            boundary_bottom=boundary_bottom
        )

        # Initialize ball
        self.ball = Ball(
            x=screen_width // 2,
            y=screen_height // 2,
            speed_x=ball_speed,
            speed_y=ball_speed,
            radius=ball_radius
        )

        # Initialize AI
        self.ai = AI(paddle=self.ai_paddle, difficulty=ai_difficulty)

    def update(self):
        """
        Updates the game state, including moving the ball, checking for collisions, and updating
        the AI paddle position.
        """
        self.ball.move()
        self.ball.collide_with_paddle(self.player_paddle)
        self.ball.collide_with_paddle(self.ai_paddle)
        self.ball.collide_with_boundaries(0, self.screen_height)
        self.ai.update(self.ball)
        self.check_score()

    def check_score(self):
        """
        Checks the score and updates it if the ball goes past the paddles.
        """
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        if self.ball.x < 0:
            self.ai_score += 1
            self.ball.reset(center_x, center_y)
        elif self.ball.x > self.screen_width:
            self.player_score += 1
            self.ball.reset(center_x, center_y)

    def reset(self):
        """
        Resets the game to the initial state.
        """
        self.player_score = 0
        self.ai_score = 0
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        self.ball.reset(center_x, center_y)

    def is_game_over(self):
        """
        Checks if the game is over based on the scores.

        :return: True if the game is over, False otherwise.
        """
        return self.player_score >= self.max_score or self.ai_score >= self.max_score

    def get_scores(self):
        """
        Returns the current scores of the player and the AI.

        :return: A tuple containing the player's score and the AI's score.
        """
        return self.player_score, self.ai_score

    def move_player_paddle_up(self):
        """
        Moves the player paddle up.
        """
        self.player_paddle.move_up()

    def move_player_paddle_down(self):
        """
        Moves the player paddle down.
        """
        self.player_paddle.move_down()
