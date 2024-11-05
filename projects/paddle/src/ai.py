# ai.py
from paddle import Paddle
from ball import Ball

class AI:
    """
    AI class represents the AI opponent. It includes methods for updating the AI paddle's position
    based on the ball's movement and the selected difficulty level to ensure the game is engaging
    for the player.
    """
    def __init__(self, paddle: Paddle, difficulty: int):
        """
        Initializes a new AI object.

        :param paddle: The Paddle object controlled by the AI.
        :param difficulty: The difficulty level of the AI, affecting its reaction speed.
        """
        self.paddle = paddle
        self.difficulty = difficulty

    def update(self, ball: Ball):
        """
        Updates the AI paddle's position based on the ball's movement.

        :param ball: The Ball object to react to.
        """
        # Calculate the center y-position of the paddle
        paddle_center = self.paddle.y + self.paddle.height / 2

        # Move the paddle towards the ball's y-position based on the difficulty level
        # The AI's speed is now proportional to the difficulty level, making it faster
        # and more challenging at higher difficulty levels.
        if ball.y < paddle_center:
            self.paddle.y -= min(self.paddle.speed * self.difficulty, paddle_center - ball.y)
        elif ball.y > paddle_center:
            self.paddle.y += min(self.paddle.speed * self.difficulty, ball.y - paddle_center)

        # Ensure the paddle stays within the game boundaries
        self.paddle.y = max(self.paddle.y, self.paddle.boundary_top)
        self.paddle.y = min(self.paddle.y, self.paddle.boundary_bottom - self.paddle.height)
