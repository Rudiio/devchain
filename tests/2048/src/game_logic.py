import random
from game_board import GameBoard
from score_manager import ScoreManager

class GameLogic:
    def __init__(self, game_board, score_manager):
        self.game_board = game_board
        self.size = game_board.size
        self.score_manager = score_manager

    def spawn_tile(self):
        empty_tiles = [(x, y) for x in range(self.size) for y in range(self.size) if self.game_board.get_tile(x, y) == 0]
        if empty_tiles:
            x, y = random.choice(empty_tiles)
            value = random.choices([2, 4], weights=[0.9, 0.1])[0]  # 90% chance of 2, 10% chance of 4
            self.game_board.set_tile(x, y, value)

    def check_move_validity(self, direction):
        temp_board = GameBoard(self.size)
        temp_board.board = [row[:] for row in self.game_board.board]
        temp_board.move_tiles(direction)
        return not self.boards_are_equal(temp_board.board, self.game_board.board)

    def boards_are_equal(self, board1, board2):
        for x in range(self.size):
            for y in range(self.size):
                if board1[x][y] != board2[x][y]:
                    return False
        return True

    def perform_move(self, direction):
        if self.check_move_validity(direction):
            score_gained = self.game_board.move_tiles(direction)
            self.score_manager.add_score(score_gained)
            if score_gained > 0:
                self.spawn_tile()
            return True, score_gained
        else:
            return False, 0

    def check_win_condition(self):
        return any(2048 in row for row in self.game_board.board)

    def check_game_over(self):
        if not self.can_merge_or_move(self.game_board.board):
            return True
        return False

    def can_merge_or_move(self, board_array):
        for x in range(self.size):
            for y in range(self.size):
                tile_value = board_array[x][y]
                if tile_value == 0:
                    return True
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        neighbor_value = board_array[nx][ny]
                        if neighbor_value == tile_value or neighbor_value == 0:
                            return True
        return False
