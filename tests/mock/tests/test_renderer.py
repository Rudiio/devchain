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
        self.game_manager.score = 2048
        self.assertTrue(self.game_manager.check_win_condition())

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.game_board = GameBoard()

    def test_initialize_grid(self):
        self.game_board.initialize_grid()
        non_empty_cells = sum(1 for row in self.game_board.grid for value in row if value)
        self.assertEqual(non_empty_cells, 2)

    def test_add_new_number(self):
        self.game_board.initialize_grid()
        initial_non_empty_cells = sum(1 for row in self.game_board.grid for value in row if value)
        self.game_board.add_new_number()
        new_non_empty_cells = sum(1 for row in self.game_board.grid for value in row if value)
        self.assertEqual(new_non_empty_cells, initial_non_empty_cells + 1)

    def test_can_merge(self):
        self.game_board.grid = [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertTrue(self.game_board.can_merge())

    def test_merge_blocks(self):
        self.game_board.grid = [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        with patch.object(self.game_board, 'merge_blocks') as mock_merge_blocks:
            self.game_board.move_blocks('UP')
            mock_merge_blocks.assert_called_once()

    def test_move_blocks(self):
        self.game_board.grid = [[2, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.game_board.move_blocks('UP')
        self.assertEqual(self.game_board.grid[0][0], 4)

    def test_has_valid_moves(self):
        self.game_board.grid = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4096], [8192, 16384, 32768, 65536]]
        self.assertFalse(self.game_board.has_valid_moves())

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()

    def test_get_direction(self):
        with patch('pygame.event.get', return_value=[{'type': pygame.KEYDOWN, 'key': pygame.K_UP}]):
            direction = self.input_handler.get_direction()
            self.assertEqual(direction, 'UP')

if __name__ == '__main__':
    unittest.main()
