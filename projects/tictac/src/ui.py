import pygame
from button import Button
from label import Label

class UI:
    def __init__(self, main):
        self.main = main
        self.new_game_button = None
        self.status_label = None
        self.create_new_game_button()
        self.create_status_label()

    def create_new_game_button(self):
        button_position = (50, 50)  # Example position, adjust as needed
        button_size = (150, 50)  # Example size, adjust as needed
        button_text = "New Game"
        self.new_game_button = Button(button_position, button_size, button_text, self.main.start_new_game)

    def create_status_label(self):
        label_position = (50, 120)  # Example position, adjust as needed
        label_text = "Player X's turn"  # Example initial text, adjust as needed
        self.status_label = Label(label_position, label_text)

    def update_status(self, message):
        self.status_label.set_text(message)
        # Removed the draw call from here to avoid redundant drawing

    def handle_click(self, position):
        if self.new_game_button.is_hovered(position):
            self.new_game_button.click()
        else:
            # Determine the board cell that was clicked
            cell_position = self.main.renderer.get_cell_from_position(position)
            if cell_position is not None:
                # Check if the cell is empty before making a move
                if self.main.game.game_board.is_cell_empty(cell_position):
                    if self.main.game.player_move(cell_position):
                        # Update the status label after a successful move
                        current_turn = self.main.game.game_board.get_current_turn()
                        self.update_status(f"Player {current_turn}'s turn")
                    else:
                        # If the move was not successful, it might be because the game is over
                        if self.main.game.check_game_over():
                            winner = self.main.game.game_board.check_winner()
                            if winner:
                                self.update_status(f"Player {winner} wins!")
                            else:
                                self.update_status("It's a draw!")
                        else:
                            # If the game is not over, it means the cell was not empty
                            self.update_status("Cell is not empty. Choose another cell.")
