class GameManager:
    """
    Manages the game state, score, win/loss conditions, and game resets.
    """

    def __init__(self, renderer=None):
        """
        Initializes the GameManager with a score of 0 and game over flag set to False.
        Optionally takes a Renderer object to update the visual state.
        """
        self.score = 0
        self.is_game_over = False
        self.renderer = renderer

    def check_win_condition(self, grid):
        """
        Checks if the win condition (2048 block) is met.

        Parameters:
        - grid: The current state of the game grid.

        Returns:
        - True if a block with the number 2048 is found, False otherwise.
        """
        for row in grid:
            if 2048 in row:
                self.is_game_over = True
                if self.renderer:
                    self.renderer.render_end_game_message("You Win!")
                return True
        return False

    def update_score(self, merged_value):
        """
        Updates the score by adding the value of merged blocks and notifies the renderer.

        Parameters:
        - merged_value: The sum of the numbers of the blocks that merged.
        """
        self.score += merged_value
        if self.renderer:
            self.renderer.render_score(self.score)

    def reset_game(self, game_board):
        """
        Resets the game to the initial state.

        Parameters:
        - game_board: The GameBoard object to reset.
        """
        self.score = 0
        self.is_game_over = False
        game_board.initialize_grid()
        if self.renderer:
            self.renderer.render_score(self.score)
            self.renderer.render_grid(game_board.grid)

    def check_game_over(self, game_board):
        """
        Checks if the game is over, which happens when no valid moves are left.

        Parameters:
        - game_board: The GameBoard object to check for valid moves.

        Returns:
        - True if no valid moves are left, False otherwise.
        """
        if not game_board.has_valid_moves():
            self.is_game_over = True
            if self.renderer:
                self.renderer.render_end_game_message("Game Over!")
            return True
        return False
