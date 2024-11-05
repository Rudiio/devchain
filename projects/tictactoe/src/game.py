from player import Player
from board import Board
from symbol import Symbol
from game_status import GameStatus

class Game:
    def __init__(self, player1, player2):
        self._current_player_index = 0
        self._players = [player1, player2]
        self._board = Board()
        self._status = GameStatus.IN_PROGRESS

    def start_game(self):
        self._board.reset_board()
        self._status = GameStatus.IN_PROGRESS
        self._current_player_index = 0

    def switch_player(self):
        self._current_player_index = 1 - self._current_player_index

    def make_move(self, row, col):
        current_player = self._players[self._current_player_index]
        if self._board.place_symbol(row, col, current_player.get_symbol()):
            if self.check_winner(current_player.get_symbol()):
                self._status = GameStatus.X_WON if current_player.get_symbol() == Symbol.X else GameStatus.O_WON
            elif self.check_draw():
                self._status = GameStatus.DRAW
            else:
                self.switch_player()
            return True
        return False

    def check_winner(self, symbol):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(self._board.get_cell(i, j).get_symbol() == symbol for j in range(3)) or \
               all(self._board.get_cell(j, i).get_symbol() == symbol for j in range(3)):
                return True
        if all(self._board.get_cell(i, i).get_symbol() == symbol for i in range(3)) or \
           all(self._board.get_cell(i, 2 - i).get_symbol() == symbol for i in range(3)):
            return True
        return False

    def check_draw(self):
        for row in range(3):
            for col in range(3):
                if self._board.is_cell_empty(row, col):
                    return False
        return True

    def get_game_status(self):
        return self._status

    def get_symbol_at(self, row, col):
        cell = self._board.get_cell(row, col)
        return cell.get_symbol() if cell else None
