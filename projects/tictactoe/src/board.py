from cell import Cell
from symbol import Symbol

class Board:
    def __init__(self):
        self._cells = [[Cell() for _ in range(3)] for _ in range(3)]

    def reset_board(self):
        for row in self._cells:
            for cell in row:
                cell.set_symbol(Symbol.EMPTY)

    def is_cell_empty(self, row, col):
        return self._cells[row][col].is_empty()

    def place_symbol(self, row, col, symbol):
        if self.is_cell_empty(row, col):
            self._cells[row][col].set_symbol(symbol)
            return True
        return False

    def get_cell(self, row, col):
        return self._cells[row][col]
