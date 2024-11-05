import pygame

class Paddle:
    """
    Paddle class defines the paddle object, including its properties like position and speed,
    and methods for movement (up and down). It also includes a method to draw the paddle using
    the Renderer, and collision detection with the ball.
    """
    def __init__(self, x, y, speed, height, width, boundary_top, boundary_bottom):
        """
        Initializes a new Paddle object.

        :param x: The x-coordinate of the paddle.
        :param y: The y-coordinate of the paddle.
        :param speed: The speed at which the paddle moves.
        :param height: The height of the paddle.
        :param width: The width of the paddle.
        :param boundary_top: The top boundary of the paddle's movement.
        :param boundary_bottom: The bottom boundary of the paddle's movement.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.height = height
        self.width = width
        self.boundary_top = boundary_top
        self.boundary_bottom = boundary_bottom

    def move_up(self):
        """
        Moves the paddle up by its speed, ensuring it doesn't go above the top boundary.
        """
        self.y = max(self.y - self.speed, self.boundary_top)

    def move_down(self):
        """
        Moves the paddle down by its speed, ensuring it doesn't go below the bottom boundary.
        """
        self.y = min(self.y + self.speed, self.boundary_bottom - self.height)

    def draw(self, renderer):
        """
        Draws the paddle on the screen using the Renderer.

        :param renderer: The Renderer object used to draw the paddle.
        """
        renderer.draw_paddle(self)

    def get_rect(self):
        """
        Gets the rectangle representing the paddle's current position and size.

        :return: A pygame.Rect object representing the paddle's current position and size.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
