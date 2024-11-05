# test_gameplay_and_scoring.py

import pytest
from src.game_app import GameApp
from src.snake import Snake

# Constants for initial game setup
INITIAL_SCORE = 0
INITIAL_SNAKE_LENGTH = 3  # Assuming this is the initial length of the snake
INITIAL_SNAKE_SPEED = 5   # Assuming this is the initial speed of the snake

@pytest.fixture
def game_app():
    # Setup for GameApp with predefined screen width and height
    game = GameApp(800, 600)
    return game

def test_game_reset_after_game_over(game_app):
    """
    Test to verify that the GameApp class resets the game correctly after a game over.
    This includes resetting the score and returning the snake to its initial length and position.
    """
    # Simulate game over scenario
    game_app.game_over = True
    game_app.score = 10  # Assuming the score is 10 at game over
    game_app.snake = Snake(5, INITIAL_SNAKE_SPEED)  # Assuming the snake grew to length 5

    # Call the end_game method to reset the game
    game_app.end_game()

    # Check if the score has been reset to 0
    assert game_app.score == INITIAL_SCORE, "Score was not reset to 0 after game over."

    # Check if the snake has been reset to its initial length
    assert len(game_app.snake.segments) == INITIAL_SNAKE_LENGTH, \
        f"Snake was not reset to initial length of {INITIAL_SNAKE_LENGTH} after game over."

    # Check if the snake's position has been reset to the initial position
    # Assuming the initial position is at the center of the screen
    initial_position = (game_app.screen_width // 2, game_app.screen_height // 2)
    head_position = game_app.snake.get_head_position()
    assert head_position == initial_position, \
        "Snake's head position was not reset to the initial position after game over."

# Additional tests can be added here to cover more scenarios and edge cases.
