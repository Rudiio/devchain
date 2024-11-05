# Architecture
## Stack
```yaml
backend:
    languages: python
    libraries:
        - pygame
frontend: {}
```
## Class diagram
```mermaid
classDiagram
    class Game {
        -int score
        -bool game_over
        -int grid_size_x
        -int grid_size_y
        -int cell_size
        -Snake snake
        -Food food
        +Game(int grid_size_x, int grid_size_y, int cell_size) Game
        +start_game() void
        +end_game() void
        +update() void
        +render(pygame.Surface screen) void
        +handle_input(Direction direction) void
        +increase_score(int amount) void
        +is_game_over() bool
        +get_score() int
        +render_score(pygame.Surface screen) void
    }
    class Snake {
        -int initial_length
        -int grid_size_x
        -int grid_size_y
        -list[Segment] body
        -Direction direction
        -bool growing
        -bool has_grown
        +Snake(int initial_length, int grid_size_x, int grid_size_y) Snake
        +move() void
        +grow() void
        +check_collision(int grid_size_x, int grid_size_y) bool
        +set_direction(Direction new_direction) void
        +get_head_position() tuple
        +get_body() list[Segment]
        +reset() void
    }
    class Segment {
        -int x
        -int y
        +Segment(int x, int y) Segment
        +set_position(int x, int y) void
        +get_position() tuple
    }
    class Food {
        -int _x
        -int _y
        -int _grid_size_x
        -int _grid_size_y
        +Food(int grid_size_x, int grid_size_y) Food
        +spawn(list[Segment] snake_body) void
        +get_position() tuple
        +__str__() string
    }
    class Direction {
        <<enumeration>>
        UP
        DOWN
        LEFT
        RIGHT
    }
    Game "1" -- "1" Snake : contains
    Game "1" -- "1" Food : contains
    Snake "1" -- "*" Segment : consists_of
```

## Front-end design
The application does not require a front-end, render directly in the back-end using the suited library.

## File list
Here are the files that the development team will need to write for the implementation of the Serpentine Feast application, considering the provided technical stack and architecture:

- /app.py (contains Game class): This file is the entry point of the application. It includes the Game class which manages the game loop, rendering, and user input. It also contains the main function to initialize the game and start the game loop using Pygame.

- /entities/snake.py (contains Snake class): This file defines the Snake class that represents the snake in the game. It includes methods for moving the snake, growing it when it eats food, checking for collisions, and changing its direction.

- /entities/segment.py (contains Segment class): This file defines the Segment class that represents each segment of the snake's body. It includes methods to set and get the position of the segment.

- /entities/food.py (contains Food class): This file defines the Food class that represents the food object in the game. It includes methods to spawn food in a random location that is not occupied by the snake.

- /utilities/direction.py (contains Direction enumeration): This file defines the Direction enumeration that represents the possible directions the snake can move in the game.

Each of these files will contain the necessary class definitions and methods as outlined in the provided backend architecture. The use of Pygame will be integrated within these classes, particularly within the Game class for rendering and input handling, and the Food class for spawning food using Pygame's capabilities. The Snake and Segment classes will primarily deal with game logic and state management.

