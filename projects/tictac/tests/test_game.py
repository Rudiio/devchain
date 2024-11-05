import unittest
from projects.tictac.src.game import Game
from projects.tictac.src.game_board import GameBoard

class TestTicTacToeGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initialization(self):
        self.assertEqual(self.game.score, {'X': 0, 'O': 0})
        self.assertIsInstance(self.game.game_board, GameBoard)
        self.assertFalse(self.game.is_game_over)

    def test_start_new_game(self):
        # Simulate a game scenario
        self.game.player_move((0, 0))  # X's turn
        self.game.player_move((1, 1))  # O's turn
        self.game.start_new_game()
        self.assertEqual(self.game.score, {'X': 0, 'O': 0})
        self.assertFalse(self.game.is_game_over)
        self.assertTrue(self.game.game_board.is_cell_empty((0, 0)))
        self.assertTrue(self.game.game_board.is_cell_empty((1, 1)))

    def test_player_move(self):
        self.assertTrue(self.game.player_move((0, 0)))  # X's turn
        self.assertFalse(self.game.game_board.is_cell_empty((0, 0)))
        self.assertEqual(self.game.game_board.get_current_turn(), 'O')
        self.assertFalse(self.game.player_move((0, 0)))  # Cell is not empty
        self.assertTrue(self.game.player_move((1, 1)))  # O's turn
        self.assertEqual(self.game.game_board.get_current_turn(), 'X')

    def test_update_score_and_check_winner(self):
        # Simulate a winning scenario for X
        self.game.player_move((0, 0))  # X's turn
        self.game.player_move((1, 0))  # O's turn
        self.game.player_move((0, 1))  # X's turn
        self.game.player_move((1, 1))  # O's turn
        self.game.player_move((0, 2))  # X wins
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.score, {'X': 1, 'O': 0})

    def test_check_draw(self):
        # Simulate a draw scenario
        moves = [(0, 0), (0, 1), (0, 2),
                 (1, 1), (1, 0), (1, 2),
                 (2, 0), (2, 2), (2, 1)]
        for move in moves:
            self.game.player_move(move)
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.score, {'X': 0, 'O': 0})

    def test_get_score(self):
        self.assertEqual(self.game.get_score(), {'X': 0, 'O': 0})
        # Simulate a winning scenario for X
        self.game.player_move((0, 0))  # X's turn
        self.game.player_move((1, 0))  # O's turn
        self.game.player_move((0, 1))  # X's turn
        self.game.player_move((1, 1))  # O's turn
        self.game.player_move((0, 2))  # X wins
        self.assertEqual(self.game.get_score(), {'X': 1, 'O': 0})

    def test_check_game_over(self):
        self.assertFalse(self.game.check_game_over())
        # Simulate a winning scenario for X
        self.game.player_move((0, 0))  # X's turn
        self.game.player_move((1, 0))  # O's turn
        self.game.player_move((0, 1))  # X's turn
        self.game.player_move((1, 1))  # O's turn
        self.game.player_move((0, 2))  # X wins
        self.assertTrue(self.game.check_game_over())

if __name__ == '__main__':
    unittest.main()
