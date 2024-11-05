import pygame

class Ball:
    """
    Ball class defines the ball object, including its properties like position, speed, and radius,
    and methods for movement and collision detection with paddles and boundaries. It also includes
    a method to draw the ball using the Renderer.
    """
    def __init__(self, x, y, speed_x, speed_y, radius):
        """
        Initializes a new Ball object.

        :param x: The x-coordinate of the ball's starting position.
        :param y: The y-coordinate of the ball's starting position.
        :param speed_x: The horizontal speed of the ball.
        :param speed_y: The vertical speed of the ball.
        :param radius: The radius of the ball.
        """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius

    def move(self):
        """
        Moves the ball by its speed in both the x and y directions.
        """
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, renderer):
        """
        Draws the ball on the screen using the Renderer.

        :param renderer: The Renderer object used to draw the ball.
        """
        renderer.draw_ball(self)

    def collide_with_paddle(self, paddle):
        """
        Checks for collision with a paddle and reflects the ball's direction if a collision is detected.

        :param paddle: The Paddle object to check for collision with.
        """
        if self.get_rect().colliderect(paddle.get_rect()):
            self.speed_x = -self.speed_x  # Reflect the horizontal direction

    def collide_with_boundaries(self, boundary_top, boundary_bottom):
        """
        Checks for collision with the top and bottom boundaries and reflects the ball's direction if a collision is detected.

        :param boundary_top: The top boundary of the playing area.
        :param boundary_bottom: The bottom boundary of the playing area.
        """
        if self.y - self.radius <= boundary_top or self.y + self.radius >= boundary_bottom:
            self.speed_y = -self.speed_y  # Reflect the vertical direction

    def reset(self, reset_x, reset_y):
        """
        Resets the ball to a specified position and reverses its horizontal direction.

        :param reset_x: The x-coordinate of the ball's reset position.
        :param reset_y: The y-coordinate of the ball's reset position.
        """
        self.x = reset_x
        self.y = reset_y
        self.speed_x = -self.speed_x  # Reverse the horizontal direction

    def increase_speed(self):
        """
        Increases the ball's speed slightly in both the x and y directions to make the game more challenging over time.
        """
        self.speed_x *= 1.1
        self.speed_y *= 1.1

    def get_rect(self):
        """
        Gets the rectangle representing the ball's current position and size.

        :return: A pygame.Rect object representing the ball's current position and size.
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
