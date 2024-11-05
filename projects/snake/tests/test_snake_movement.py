import pytest
from src.snake import Snake
from src.segment import Segment

# Constants for the tests
INITIAL_LENGTH = 5
SPEED = 1
INITIAL_DIRECTION = 'right'

@pytest.fixture
def snake():
    """Fixture to create a new snake for each test."""
    return Snake(INITIAL_LENGTH, SPEED)

def test_snake_initial_direction(snake):
    """Test that the snake's initial direction is set correctly."""
    assert snake.direction == INITIAL_DIRECTION, "Initial direction should be 'right'."

def test_snake_change_direction(snake):
    """Test that the snake's direction changes correctly."""
    directions = ['up', 'left', 'down', 'right']
    for new_direction in directions:
        snake.change_direction(new_direction)
        assert snake.direction == new_direction, f"Snake direction should be '{new_direction}' after change."

def test_snake_move(snake):
    """Test that the snake moves correctly in the initial direction."""
    initial_head_position = snake.get_head_position()
    snake.move()
    new_head_position = snake.get_head_position()
    assert new_head_position == (initial_head_position[0] + SPEED, initial_head_position[1]), "Snake should move to the right."

def test_snake_move_with_direction_change(snake):
    """Test that the snake moves correctly after changing direction."""
    # Change direction to 'down'
    snake.change_direction('down')
    initial_head_position = snake.get_head_position()
    snake.move()
    new_head_position = snake.get_head_position()
    assert new_head_position == (initial_head_position[0], initial_head_position[1] + SPEED), "Snake should move down."

def test_snake_rapid_direction_changes(snake):
    """Test that the snake responds correctly to rapid direction changes."""
    # Simulate rapid direction changes
    snake.change_direction('up')
    snake.change_direction('left')
    snake.change_direction('down')
    snake.move()
    # The snake should only move in the last direction set before the move
    initial_head_position = snake.get_head_position()
    assert initial_head_position == (INITIAL_LENGTH - 1, SPEED), "Snake should move down after rapid direction changes."

def test_snake_move_does_not_allow_reverse(snake):
    """Test that the snake does not move in the reverse direction."""
    # Attempt to change to the reverse direction
    snake.change_direction('left')
    snake.move()
    # The snake should not move left as it is the reverse of the initial direction 'right'
    new_head_position = snake.get_head_position()
    assert new_head_position != (INITIAL_LENGTH - 1 - SPEED, 0), "Snake should not move in the reverse direction."

# Add more tests as needed to cover different scenarios and edge cases.
