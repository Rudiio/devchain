import unittest
from unittest.mock import Mock
from paddle.src.ball import Ball
from paddle.src.paddle import Paddle

class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(x=50, y=50, speed_x=5, speed_y=5, radius=10)

    def test_initialization(self):
        self.assertEqual(self.ball.x, 50)
        self.assertEqual(self.ball.y, 50)
        self.assertEqual(self.ball.speed_x, 5)
        self.assertEqual(self.ball.speed_y, 5)
        self.assertEqual(self.ball.radius, 10)

    def test_move(self):
        initial_x = self.ball.x
        initial_y = self.ball.y
        self.ball.move()
        self.assertEqual(self.ball.x, initial_x + self.ball.speed_x)
        self.assertEqual(self.ball.y, initial_y + self.ball.speed_y)

    def test_collide_with_paddle(self):
        paddle = Paddle(x=40, y=40, speed=0, height=20, width=10, boundary_top=0, boundary_bottom=100)
        self.ball.x = 45  # Position the ball to collide with the paddle
        self.ball.collide_with_paddle(paddle)
        self.assertEqual(self.ball.speed_x, -5)  # Speed should be reversed

    def test_collide_with_boundaries(self):
        boundary_top = 0
        boundary_bottom = 100
        self.ball.y = boundary_top + self.ball.radius  # Position the ball to collide with the top boundary
        self.ball.collide_with_boundaries(boundary_top, boundary_bottom)
        self.assertEqual(self.ball.speed_y, 5)  # Speed should be reversed

        self.ball.y = boundary_bottom - self.ball.radius  # Position the ball to collide with the bottom boundary
        self.ball.collide_with_boundaries(boundary_top, boundary_bottom)
        self.assertEqual(self.ball.speed_y, -5)  # Speed should be reversed

    def test_reset(self):
        reset_x = 100
        reset_y = 100
        self.ball.reset(reset_x, reset_y)
        self.assertEqual(self.ball.x, reset_x)
        self.assertEqual(self.ball.y, reset_y)
        self.assertEqual(self.ball.speed_x, -5)  # Speed should be reversed

    def test_increase_speed(self):
        initial_speed_x = self.ball.speed_x
        initial_speed_y = self.ball.speed_y
        self.ball.increase_speed()
        self.assertEqual(self.ball.speed_x, initial_speed_x * 1.1)
        self.assertEqual(self.ball.speed_y, initial_speed_y * 1.1)

    def test_get_rect(self):
        expected_rect = (self.ball.x - self.ball.radius, self.ball.y - self.ball.radius, self.ball.radius * 2, self.ball.radius * 2)
        self.assertEqual(self.ball.get_rect(), expected_rect)

if __name__ == '__main__':
    unittest.main()
