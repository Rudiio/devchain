import unittest
from unittest.mock import Mock
from paddle.src.game import Game
from paddle.src.paddle import Paddle
from paddle.src.ball import Ball
from paddle.src.ai import AI

class TestGame(unittest.TestCase):
    def setUp(self):
        self.max_score = 10
        self.game = Game(self.max_score)
        self.game.initialize_game_elements(
            screen_width=800,
            screen_height=600,
            paddle_width=10,
            paddle_height=100,
            ball_radius=5,
            paddle_speed=5,
            ball_speed=5,
            ai_difficulty=1
        )

    def test_initialization(self):
        self.assertEqual(self.game.player_score, 0)
        self.assertEqual(self.game.ai_score, 0)
        self.assertEqual(self.game.max_score, self.max_score)
        self.assertIsInstance(self.game.player_paddle, Paddle)
        self.assertIsInstance(self.game.ai_paddle, Paddle)
        self.assertIsInstance(self.game.ball, Ball)
        self.assertIsInstance(self.game.ai, AI)

    def test_move_player_paddle_up(self):
        initial_y = self.game.player_paddle.y
        self.game.move_player_paddle_up()
        self.assertLess(self.game.player_paddle.y, initial_y)

    def test_move_player_paddle_down(self):
        initial_y = self.game.player_paddle.y
        self.game.move_player_paddle_down()
        self.assertGreater(self.game.player_paddle.y, initial_y)

    def test_update_score_when_ball_missed_by_player(self):
        self.game.ball.x = -1  # Simulate ball going past the player paddle
        self.game.check_score()
        self.assertEqual(self.game.ai_score, 1)
        self.assertEqual(self.game.player_score, 0)

    def test_update_score_when_ball_missed_by_ai(self):
        self.game.ball.x = self.game.screen_width + 1  # Simulate ball going past the AI paddle
        self.game.check_score()
        self.assertEqual(self.game.player_score, 1)
        self.assertEqual(self.game.ai_score, 0)

    def test_reset_game(self):
        self.game.player_score = 5
        self.game.ai_score = 3
        self.game.reset()
        self.assertEqual(self.game.player_score, 0)
        self.assertEqual(self.game.ai_score, 0)

    def test_is_game_over(self):
        self.game.player_score = self.max_score
        self.assertTrue(self.game.is_game_over())

    def test_is_game_not_over(self):
        self.game.player_score = self.max_score - 1
        self.assertFalse(self.game.is_game_over())

    def test_get_scores(self):
        self.game.player_score = 2
        self.game.ai_score = 3
        player_score, ai_score = self.game.get_scores()
        self.assertEqual(player_score, 2)
        self.assertEqual(ai_score, 3)

    def test_ball_reset_after_score(self):
        self.game.ball.x = -1  # Simulate ball going past the player paddle
        self.game.check_score()
        self.assertEqual(self.game.ball.x, self.game.screen_width // 2)
        self.assertEqual(self.game.ball.y, self.game.screen_height // 2)

if __name__ == '__main__':
    unittest.main()
