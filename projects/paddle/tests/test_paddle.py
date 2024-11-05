import unittest
from paddle.src.paddle import Paddle

class TestPaddle(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(x=50, y=100, speed=10, height=50, width=10, boundary_top=0, boundary_bottom=300)

    def test_initialization(self):
        self.assertEqual(self.paddle.x, 50)
        self.assertEqual(self.paddle.y, 100)
        self.assertEqual(self.paddle.speed, 10)
        self.assertEqual(self.paddle.height, 50)
        self.assertEqual(self.paddle.width, 10)
        self.assertEqual(self.paddle.boundary_top, 0)
        self.assertEqual(self.paddle.boundary_bottom, 300)

    def test_move_up_within_boundaries(self):
        self.paddle.y = 50
        self.paddle.move_up()
        self.assertEqual(self.paddle.y, 40)

    def test_move_up_at_boundary(self):
        self.paddle.y = 0
        self.paddle.move_up()
        self.assertEqual(self.paddle.y, 0)

    def test_move_down_within_boundaries(self):
        self.paddle.y = 200
        self.paddle.move_down()
        self.assertEqual(self.paddle.y, 210)

    def test_move_down_at_boundary(self):
        self.paddle.y = self.paddle.boundary_bottom - self.paddle.height
        self.paddle.move_down()
        self.assertEqual(self.paddle.y, self.paddle.boundary_bottom - self.paddle.height)

    def test_get_rect(self):
        rect = self.paddle.get_rect()
        self.assertEqual(rect.x, self.paddle.x)
        self.assertEqual(rect.y, self.paddle.y)
        self.assertEqual(rect.width, self.paddle.width)
        self.assertEqual(rect.height, self.paddle.height)

if __name__ == '__main__':
    unittest.main()
