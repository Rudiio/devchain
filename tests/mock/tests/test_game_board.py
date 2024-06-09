import unittest
from unittest.mock import Mock
from mock.src.game_board import GameBoard
from mock.src.game_manager import GameManager

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.game_manager = Mock(spec=GameManager)
        self.game_board = GameBoard(self.game_manager)

    def test_initialize_grid(self):
        self.game_board.initialize_grid()
        non_zero_count = sum(cell != 0 for row in self.game_board.grid for cell in row)
        self.assertEqual(non_zero_count, 2)

    def test_add_new_number(self):
        self.game_board.grid = [[0] * self.game_board.size for _ in range(self.game_board.size)]
        self.game_board.add_new_number()
        non_zero_count = sum(cell != 0 for row in self.game_board.grid for cell in row)
        self.assertEqual(non_zero_count, 1)

    def test_can_merge(self):
        self.assertTrue(self.game_board.can_merge(2, 2))
        self.assertFalse(self.game_board.can_merge(2, 4))

    def test_merge_blocks(self):
        line = [2, 2, 4, 4]
        new_line, score = self.game_board.merge_blocks(line)
        self.assertEqual(new_line, [4, 8, 0, 0])
        self.assertEqual(score, 12)

    def test_move_blocks_up(self):
        self.game_board.grid = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [4, 0, 0, 0]
        ]
        moved, score = self.game_board.move_blocks('up')
        self.assertTrue(moved)
        self.assertEqual(score, 12)
        self.assertEqual(self.game_board.grid[0], [4, 0, 0, 0])

    def test_move_blocks_down(self):
        self.game_board.grid = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [4, 0, 0, 0]
        ]
        moved, score = self.game_board.move_blocks('down')
        self.assertTrue(moved)
        self.assertEqual(score, 12)
        self.assertEqual(self.game_board.grid[3], [4, 0, 0, 0])

    def test_move_blocks_left(self):
        self.game_board.grid = [
            [2, 2, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        moved, score = self.game_board.move_blocks('left')
        self.assertTrue(moved)
        self.assertEqual(score, 12)
        self.assertEqual(self.game_board.grid[0][:2], [4, 8])

    def test_move_blocks_right(self):
        self.game_board.grid = [
            [2, 2, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        moved, score = self.game_board.move_blocks('right')
        self.assertTrue(moved)
        self.assertEqual(score, 12)
        self.assertEqual(self.game_board.grid[0][-2:], [8, 4])

    def test_has_valid_moves(self):
        self.game_board.grid = [[0] * self.game_board.size for _ in range(self.game_board.size)]
        self.assertTrue(self.game_board.has_valid_moves())

        self.game_board.grid = [[2] * self.game_board.size for _ in range(self.game_board.size)]
        self.assertFalse(self.game_board.has_valid_moves())

        self.game_board.grid[0][0] = 0
        self.assertTrue(self.game_board.has_valid_moves())

        self.game_board.grid[0][0] = 4
        self.game_board.grid[0][1] = 4
        self.assertTrue(self.game_board.has_valid_moves())

if __name__ == '__main__':
    unittest.main()
