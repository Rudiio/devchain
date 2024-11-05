import random

class GameBoard:
    """
    Manages the game grid for the 2048-like game, including block placement, merging, and movement.
    """
    
    def __init__(self, game_manager, size=4):
        """
        Initializes the game board with a given size and a reference to the GameManager.
        The size is set to 10 to match the game requirements.
        """
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.game_manager = game_manager
        self.initialize_grid()

    def initialize_grid(self):
        """
        Resets the grid to the starting state with two numbers placed randomly.
        """
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.add_new_number()
        self.add_new_number()

    def add_new_number(self):
        """
        Adds a new number (2 or 4) to a random empty spot on the grid.
        """
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def can_merge(self, a, b):
        """
        Checks if two blocks can merge (i.e., have the same number).
        """
        return a == b

    def merge_blocks(self, line):
        """
        Merges blocks in a given line and returns the new line and score gained from the merge.
        This function has been updated to handle multiple merges within a single move.
        """
        new_line = []
        score = 0
        i = 0
        while i < len(line):
            if i + 1 < len(line) and self.can_merge(line[i], line[i + 1]):
                merged_value = 2 * line[i]
                new_line.append(merged_value)
                score += merged_value
                i += 2
                # Skip over the next value if it was merged
                while i < len(line) and line[i] == 0:
                    i += 1
            else:
                new_line.append(line[i])
                i += 1
        while len(new_line) < len(line):
            new_line.append(0)
        return new_line, score

    def move_blocks(self, direction):
        """
        Moves blocks in the given direction and returns a tuple indicating if any blocks were moved and the score gained from any merges.
        This function has been updated to handle all directions and return the expected tuple.
        """
        score = 0
        moved = False
        if direction in ('up', 'down'):
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size) if self.grid[i][j] != 0]
                if direction == 'down':
                    column.reverse()
                original_column = list(column)  # Copy the original column for comparison
                merged_column, column_score = self.merge_blocks(column)
                if direction == 'down':
                    merged_column.reverse()
                for i in range(self.size):
                    self.grid[i][j] = merged_column[i] if i < len(merged_column) else 0
                score += column_score
                if original_column != merged_column:
                    moved = True
        elif direction in ('left', 'right'):
            for i in range(self.size):
                row = [self.grid[i][j] for j in range(self.size) if self.grid[i][j] != 0]
                if direction == 'right':
                    row.reverse()
                original_row = list(row)  # Copy the original row for comparison
                merged_row, row_score = self.merge_blocks(row)
                if direction == 'right':
                    merged_row.reverse()
                self.grid[i] = merged_row + [0] * (self.size - len(merged_row))
                score += row_score
                if original_row != merged_row:
                    moved = True

        if moved:
            self.add_new_number()
            self.game_manager.update_score(score)
        return moved, score  # Return a tuple with the moved status and score

    def has_valid_moves(self):
        """
        Checks if there are any valid moves left on the board.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return True
                if i + 1 < self.size and self.can_merge(self.grid[i][j], self.grid[i + 1][j]):
                    return True
                if j + 1 < self.size and self.can_merge(self.grid[i][j], self.grid[i][j + 1]):
                    return True
        return False
