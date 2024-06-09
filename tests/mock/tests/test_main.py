import unittest
from unittest.mock import patch
from mock.src.game_manager import GameManager
from mock.src.game_board import GameBoard
from mock.src.input_handler import InputHandler

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.game_manager = GameManager()

    def test_reset_game(self):
        self.game_manager.score = 100
        self.game_manager.is_game_over = True
        self.game_manager.reset_game()
        self.assertEqual(self.game_manager.score, 0)
        self.assertFalse(self.game_manager.is_game_over)

    def test_update_score(self):
        initial_score = self.game_manager.score
        self.game_manager.update_score(4)
        self.assertEqual(self.game_manager.score, initial_score + 4)

    def test_check_win_condition(self):
        grid = [[0] * 10 for _ in range(10)]
        grid[0][0] = 2048
        self.assertTrue(self.game_manager.check_win_condition(grid))

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.game_manager = GameManager()
        self.game_board = GameBoard(self.game_manager)

    def test_initialize_grid(self):
        self.game_board.initialize_grid()
        non_zero_count = sum(cell != 0 for row in self.game_board.grid for cell in row)
        self.assertEqual(non_zero_count, 2)

    def test_add_new_number(self):
        self.game_board.grid = [[0] * 10 for _ in range(10)]
        self.game_board.add_new_number()
        non_zero_count = sum(cell != 0 for row in self.game_board.grid for cell in row)
        self.assertEqual(non_zero_count, 1)

    def test_can_merge(self):
        self.game_board.grid = [[2, 2] + [0] * 8, [4, 4] + [0] * 8] + [[0] * 10 for _ in range(8)]
        self.assertTrue(self.game_board.can_merge())

    def test_merge_blocks(self):
        self.game_board.grid = [[2, 2] + [0] * 8, [4, 4] + [0] * 8] + [[0] * 10 for _ in range(8)]
        self.game_board.merge_blocks()
        self.assertEqual(self.game_board.grid[0][0], 4)
        self.assertEqual(self.game_board.grid[1][0], 8)

    def test_move_blocks(self):
        self.game_board.grid = [[2, 0, 2, 0] + [0] * 6, [0] * 10, [0] * 10, [0] * 10] + [[0] * 10 for _ in range(6)]
        moved, merged_value = self.game_board.move_blocks('LEFT')
        self.assertTrue(moved)
        self.assertEqual(merged_value, 4)

    def test_has_valid_moves(self):
        self.game_board.grid = [[2] * 10 for _ in range(10)]
        self.assertFalse(self.game_board.has_valid_moves())

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()

    @patch('pygame.event.get')
    def test_get_direction(self, mock_event_get):
        mock_event_get.return_value = [MockEvent(pygame.KEYDOWN, {'key': pygame.K_UP})]
        direction = self.input_handler.get_direction(mock_event_get.return_value[0])
        self.assertEqual(direction, 'UP')

class MockEvent:
    def __init__(self, type, dict):
        self.type = type
        self.dict = dict
        self.key = self.dict.get('key', None)

if __name__ == '__main__':
    unittest.main()
