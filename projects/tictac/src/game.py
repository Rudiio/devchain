from game_board import GameBoard

class Game:
    def __init__(self):
        self.score = {'X': 0, 'O': 0}
        self.game_board = GameBoard()
        self.is_game_over = False

    def start_new_game(self):
        self.game_board.reset()
        self.is_game_over = False
        self.score = {'X': 0, 'O': 0}  # Reset the score for a new game

    def player_move(self, position):
        if not self.is_game_over and self.game_board.is_cell_empty(position):
            current_turn = self.game_board.get_current_turn()
            if self.game_board.place_symbol(position, current_turn):
                winner = self.game_board.check_winner()
                if winner:
                    self.update_score(winner)
                    self.is_game_over = True
                elif self.game_board.is_draw():
                    self.is_game_over = True
                else:
                    self.game_board.toggle_turn()
            return True
        return False

    def update_score(self, winner):
        if winner in self.score:
            self.score[winner] += 1

    def get_score(self):
        return self.score

    def check_game_over(self):
        return self.is_game_over
