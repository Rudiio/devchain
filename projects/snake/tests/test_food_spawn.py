# test_food_spawn.py
import pytest
from src.food import Food
from src.snake import Snake
from src.segment import Segment

# Constants for the tests
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SEGMENT_SIZE = 20  # Assuming a segment size for the snake

# Helper function to create a snake with segments in known positions
def create_snake_with_segments(segment_positions):
    snake = Snake(initial_length=0, speed=5)  # initial_length=0 to start with an empty snake
    for pos in segment_positions:
        snake.segments.append(Segment(pos[0], pos[1]))
    return snake

# Test that food spawns in an empty area
def test_food_spawn_empty_area():
    # Create a snake with segments occupying some positions
    snake = create_snake_with_segments([(100, 100), (120, 100), (140, 100)])

    # Create a Food instance
    food = Food()

    # Call the spawn method
    food.spawn(snake.segments, SCREEN_WIDTH, SCREEN_HEIGHT, SEGMENT_SIZE)

    # Get the position where the food spawned
    food_position = food.get_position()

    # Check that the food is not on any of the snake's segments
    for segment in snake.segments:
        assert food_position != (segment.x, segment.y), "Food spawned on a snake segment."

    # Check that the food is within the game boundaries
    assert 0 <= food_position[0] < SCREEN_WIDTH, "Food x position is out of bounds."
    assert 0 <= food_position[1] < SCREEN_HEIGHT, "Food y position is out of bounds."

# Test that food does not spawn on the snake
def test_food_does_not_spawn_on_snake():
    # Create a snake that occupies a large area of the screen
    snake = create_snake_with_segments([(x, y) for x in range(0, SCREEN_WIDTH, SEGMENT_SIZE)
                                                    for y in range(0, SCREEN_HEIGHT, SEGMENT_SIZE)])

    # Create a Food instance
    food = Food()

    # Call the spawn method multiple times to check different random positions
    for _ in range(10):
        food.spawn(snake.segments, SCREEN_WIDTH, SCREEN_HEIGHT, SEGMENT_SIZE)
        food_position = food.get_position()

        # Check that the food is not on any of the snake's segments
        assert all(food_position != (segment.x, segment.y) for segment in snake.segments), \
            "Food spawned on a snake segment."

# Test that food spawns within the screen boundaries
def test_food_spawn_within_boundaries():
    # Create an empty snake (no segments)
    snake = create_snake_with_segments([])

    # Create a Food instance
    food = Food()

    # Call the spawn method multiple times to check different random positions
    for _ in range(10):
        food.spawn(snake.segments, SCREEN_WIDTH, SCREEN_HEIGHT, SEGMENT_SIZE)
        food_position = food.get_position()

        # Check that the food is within the game boundaries
        assert 0 <= food_position[0] < SCREEN_WIDTH, "Food x position is out of bounds."
        assert 0 <= food_position[1] < SCREEN_HEIGHT, "Food y position is out of bounds."
