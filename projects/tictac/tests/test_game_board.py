import unittest
from projects.tictac.src.game_board import GameBoard

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.game_board = GameBoard()

    def test_reset(self):
        self.game_board.reset()
        self.assertEqual(self.game_board.board, [['', '', ''], ['', '', ''], ['', '', '']])
        self.assertEqual(self.game_board.current_turn, 'X')

    def test_place_symbol(self):
        self.assertTrue(self.game_board.place_symbol((0, 0), 'X'))
        self.assertEqual(self.game_board.board[0][0], 'X')
        self.assertFalse(self.game_board.place_symbol((0, 0), 'O'))
        self.assertEqual(self.game_board.board[0][0], 'X')

    def test_check_winner(self):
        # Set up a winning condition for 'X' horizontally
        self.game_board.board = [['X', 'X', 'X'], ['', '', ''], ['', '', '']]
        self.assertEqual(self.game_board.check_winner(), 'X')

        # Set up a winning condition for 'O' vertically
        self.game_board.board = [['O', '', ''], ['O', '', ''], ['O', '', '']]
        self.assertEqual(self.game_board.check_winner(), 'O')

        # Set up a winning condition for 'X' diagonally
        self.game_board.board = [['X', '', ''], ['', 'X', ''], ['', '', 'X']]
        self.assertEqual(self.game_board.check_winner(), 'X')

        # No winner
        self.game_board.board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
        self.assertIsNone(self.game_board.check_winner())

    def test_is_draw(self):
        self.game_board.board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]
        self.assertTrue(self.game_board.is_draw())

        self.game_board.board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', '', 'O']]
        self.assertFalse(self.game_board.is_draw())

    def test_get_current_turn(self):
        self.assertEqual(self.game_board.get_current_turn(), 'X')
        self.game_board.toggle_turn()
        self.assertEqual(self.game_board.get_current_turn(), 'O')

    def test_toggle_turn(self):
        self.game_board.current_turn = 'X'
        self.game_board.toggle_turn()
        self.assertEqual(self.game_board.current_turn, 'O')
        self.game_board.toggle_turn()
        self.assertEqual(self.game_board.current_turn, 'X')

    def test_is_cell_empty(self):
        self.game_board.board = [['X', '', ''], ['', '', ''], ['', '', '']]
        self.assertTrue(self.game_board.is_cell_empty((1, 0)))
        self.assertFalse(self.game_board.is_cell_empty((0, 0)))

if __name__ == '__main__':
    unittest.main()
