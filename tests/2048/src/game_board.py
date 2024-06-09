class GameBoard:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]

    def set_tile(self, x, y, value):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[x][y] = value

    def get_tile(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.board[x][y]
        return None

    def compress(self, line):
        new_line = [i for i in line if i != 0]
        new_line += [0] * (self.size - len(new_line))
        return new_line

    def merge(self, line):
        score = 0
        for i in range(self.size - 1):
            if line[i] == line[i + 1] and line[i] != 0:
                line[i] *= 2
                line[i + 1] = 0
                score += line[i]
        return score, line

    def reverse(self, line):
        return line[::-1]

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_tiles(self, direction):
        score = 0
        moves = {'up': self.move_up, 'down': self.move_down,
                 'left': self.move_left, 'right': self.move_right}
        if direction in moves:
            score = moves[direction]()
        return score

    def move_left(self):
        score = 0
        for i in range(self.size):
            compressed = self.compress(self.board[i])
            merged_score, merged = self.merge(compressed)
            score += merged_score
            self.board[i] = self.compress(merged)
        return score

    def move_right(self):
        score = 0
        for i in range(self.size):
            reversed_line = self.reverse(self.board[i])
            compressed = self.compress(reversed_line)
            merged_score, merged = self.merge(compressed)
            score += merged_score
            self.board[i] = self.reverse(self.compress(merged))
        return score

    def move_up(self):
        score = 0
        self.transpose()
        score += self.move_left()
        self.transpose()
        return score

    def move_down(self):
        score = 0
        self.transpose()
        score += self.move_right()
        self.transpose()
        return score
