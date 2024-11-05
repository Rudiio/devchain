import pytest
from src.snake import Snake
from src.segment import Segment

# Test cases for the Snake class collision with its own body

def test_snake_collision_with_itself():
    """
    Test that check_collision() returns True when the snake's head collides with any of its own body segments.
    """
    # Initialize a snake with a length of 5 segments and a speed of 1
    snake = Snake(initial_length=5, speed=1)
    
    # Manually set the snake's segments to create a collision scenario
    # The snake is moving right and will collide with its own body
    snake.segments = [
        Segment(5, 5),  # Head segment
        Segment(4, 5),
        Segment(3, 5),
        Segment(3, 4),
        Segment(4, 4),  # This segment will collide with the head
    ]
    
    # Set the direction of the snake to right
    snake.direction = 'RIGHT'
    
    # Move the snake manually to the collision point
    snake.move()
    
    # Check if the collision is detected
    assert snake.check_collision() == True, "The snake should have collided with itself."

def test_snake_no_collision_with_itself():
    """
    Test that check_collision() returns False when the snake's head does not collide with any of its own body segments.
    """
    # Initialize a snake with a length of 5 segments and a speed of 1
    snake = Snake(initial_length=5, speed=1)
    
    # Manually set the snake's segments to a scenario where there is no collision
    snake.segments = [
        Segment(5, 5),  # Head segment
        Segment(4, 5),
        Segment(3, 5),
        Segment(2, 5),
        Segment(1, 5),
    ]
    
    # Set the direction of the snake to right
    snake.direction = 'RIGHT'
    
    # Move the snake manually away from its body
    snake.move()
    
    # Check if the collision is detected
    assert snake.check_collision() == False, "The snake should not have collided with itself."

# Run the tests
if __name__ == "__main__":
    pytest.main()
