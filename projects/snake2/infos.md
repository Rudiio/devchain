# Project Informations

## Request
Snake game in python using pygame. The game should feature a green snake with a red food. Divide the screen into a grid and consider that one cell is the size of a segment of the snake and the size of a food.

## Name
Serpentine Feast

## Description
**Application Summary: Serpentine Feast**

**Overview:**
Serpentine Feast is a grid-based snake game where players control a green snake with the goal of consuming red food to grow in length. The game challenges players to maneuver the snake around the play area using the arrow keys without colliding with the walls or the snake's own body. The game is implemented in Python, utilizing the pygame library for graphical representation and control handling.

**Features and Gameplay:**

1. **Snake Movement:**
   - Players use the arrow keys (up, down, left, right) to direct the snake's movement on a grid.
   - The snake moves smoothly from one grid cell to the next, ensuring a responsive gaming experience.

2. **Snake Growth:**
   - The snake grows by one cell in length each time it consumes a red food item.
   - The red food item randomly reappears in an unoccupied cell on the grid after being eaten.

3. **Game Termination:**
   - The game ends with a "Game Over" message if the snake hits the boundary walls or collides with its own body.
   - The game area is defined by a grid that represents the boundaries within which the snake can move.

4. **Scoring System:**
   - The player's score is displayed on the screen during gameplay and increases with each red food item consumed.
   - The score increments are fixed and are designed to reflect the player's success in growing the snake.

**Technical Requirements:**

1. **Language and Library:**
   - The game is developed in Python, leveraging the pygame library for rendering graphics, handling input, and managing game state.

2. **Color Scheme:**
   - The snake is distinctly colored green, and the food is colored red, providing clear visual cues to the player.

3. **Grid System:**
   - The game screen is divided into a grid, with each cell equal to the size of one snake segment and the red food item.
   - This grid system facilitates the grid-based movement of the snake and the placement of food.

4. **Transition and Fluidity:**
   - The snake's movement from cell to cell is designed to be smooth, ensuring a visually appealing and fluid gameplay experience.

**End Goal:**
The application aims to provide an engaging and nostalgic snake game experience with a modern touch, focusing on smooth controls and gameplay. The player's objective is to achieve the highest possible score by consuming food while avoiding self-collision and wall impacts.

