class GameBoard:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'

    def place_symbol(self, position, symbol):
        if self.is_cell_empty(position):
            x, y = position
            self.board[y][x] = symbol
            return True
        return False

    def check_winner(self):
        # Check rows, columns and diagonals for a winner
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        return None

    def is_draw(self):
        return all(all(cell != '' for cell in row) for row in self.board)

    def get_current_turn(self):
        return self.current_turn

    def toggle_turn(self):
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    def is_cell_empty(self, position):
        x, y = position
        return self.board[y][x] == ''
