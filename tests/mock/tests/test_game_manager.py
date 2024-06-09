import unittest
from unittest.mock import Mock
from mock.src.game_manager import GameManager

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.renderer_mock = Mock()
        self.game_manager = GameManager(renderer=self.renderer_mock)
        self.game_board_mock = Mock()
        self.game_board_mock.grid = [[0] * 10 for _ in range(10)]

    def test_initialization(self):
        self.assertEqual(self.game_manager.score, 0)
        self.assertFalse(self.game_manager.is_game_over)
        self.assertIsNotNone(self.game_manager.renderer)

    def test_check_win_condition_not_met(self):
        self.assertFalse(self.game_manager.check_win_condition(self.game_board_mock.grid))
        self.assertFalse(self.game_manager.is_game_over)
        self.renderer_mock.render_end_game_message.assert_not_called()

    def test_check_win_condition_met(self):
        self.game_board_mock.grid[0][0] = 2048
        self.assertTrue(self.game_manager.check_win_condition(self.game_board_mock.grid))
        self.assertTrue(self.game_manager.is_game_over)
        self.renderer_mock.render_end_game_message.assert_called_once_with("You Win!")

    def test_update_score(self):
        merged_value = 16
        self.game_manager.update_score(merged_value)
        self.assertEqual(self.game_manager.score, merged_value)
        self.renderer_mock.render_score.assert_called_once_with(merged_value)

    def test_reset_game(self):
        self.game_manager.score = 50
        self.game_manager.is_game_over = True
        self.game_manager.reset_game(self.game_board_mock)
        self.assertEqual(self.game_manager.score, 0)
        self.assertFalse(self.game_manager.is_game_over)
        self.game_board_mock.initialize_grid.assert_called_once()
        self.renderer_mock.render_score.assert_called_once_with(0)
        self.renderer_mock.render_grid.assert_called_once_with(self.game_board_mock.grid)

    def test_check_game_over_no_valid_moves(self):
        self.game_board_mock.has_valid_moves.return_value = False
        self.assertFalse(self.game_manager.is_game_over)
        self.assertTrue(self.game_manager.check_game_over(self.game_board_mock))
        self.assertTrue(self.game_manager.is_game_over)
        self.renderer_mock.render_end_game_message.assert_called_once_with("Game Over!")

    def test_check_game_over_with_valid_moves(self):
        self.game_board_mock.has_valid_moves.return_value = True
        self.assertFalse(self.game_manager.is_game_over)
        self.assertFalse(self.game_manager.check_game_over(self.game_board_mock))
        self.assertFalse(self.game_manager.is_game_over)
        self.renderer_mock.render_end_game_message.assert_not_called()

if __name__ == '__main__':
    unittest.main()
