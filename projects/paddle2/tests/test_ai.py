import unittest
from unittest.mock import Mock
from paddle.src.ai import AI
from paddle.src.paddle import Paddle
from paddle.src.ball import Ball

class TestAI(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(50, 100, 10, 50, 10, 0, 400)
        self.ball = Ball(200, 200, 5, 5, 10)
        self.ai = AI(self.paddle, difficulty=1)

    def test_initialization(self):
        self.assertEqual(self.ai.paddle, self.paddle)
        self.assertEqual(self.ai.difficulty, 1)

    def test_update_ai_paddle_position_moving_up(self):
        self.ball.y = 50  # Ball is above the paddle center
        initial_paddle_y = self.paddle.y
        self.ai.update(self.ball)
        self.assertLess(self.paddle.y, initial_paddle_y)

    def test_update_ai_paddle_position_moving_down(self):
        self.ball.y = 150  # Ball is below the paddle center
        initial_paddle_y = self.paddle.y
        self.ai.update(self.ball)
        self.assertGreater(self.paddle.y, initial_paddle_y)

    def test_update_ai_paddle_position_with_high_difficulty(self):
        self.ai.difficulty = 3
        self.ball.y = 150  # Ball is below the paddle center
        initial_paddle_y = self.paddle.y
        self.ai.update(self.ball)
        expected_position = initial_paddle_y + self.paddle.speed * self.ai.difficulty
        self.assertEqual(self.paddle.y, expected_position)

    def test_ai_paddle_stays_within_boundaries_top(self):
        self.ball.y = -50  # Ball is way above the paddle and the top boundary
        self.ai.update(self.ball)
        self.assertEqual(self.paddle.y, self.paddle.boundary_top)

    def test_ai_paddle_stays_within_boundaries_bottom(self):
        self.ball.y = 500  # Ball is way below the paddle and the bottom boundary
        self.ai.update(self.ball)
        self.assertEqual(self.paddle.y, self.paddle.boundary_bottom - self.paddle.height)

if __name__ == '__main__':
    unittest.main()
