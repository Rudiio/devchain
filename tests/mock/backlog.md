# Backlog

## Name
2048 Game

## User stories
1. As a player, I want to be able to move the tiles in four directions - up, down, left, and right.
    Acceptance criteria:
    - When I press the up arrow key, the tiles should move upwards and merge if they have the same value.
    - When I press the down arrow key, the tiles should move downwards and merge if they have the same value.
    - When I press the left arrow key, the tiles should move to the left and merge if they have the same value.
    - When I press the right arrow key, the tiles should move to the right and merge if they have the same value.

2. As a player, I want the game to end when there are no more valid moves.
    Acceptance criteria:
    - If there are no empty spaces and no adjacent tiles with the same value, the game should end and display the "Game Over" message.

3. As a player, I want to reach the 2048 tile to win the game.
    Acceptance criteria:
    - When a tile with the value of 2048 is created, the player wins the game and a "You Win" message is displayed.

## Requirements
1. The game should be implemented in Python using the Pygame library for the graphical interface.

2. The tiles' movement should be smooth and responsive to the arrow key inputs.

3. The game should have a graphical interface with visual representations of the tiles and the game board.

4. The game should keep track of the player's score, which increases each time two tiles are merged.

5. The game should have a "New Game" button to start a new game after winning or losing.

6. The game should have a "Quit" button to exit the game at any time.

7. The game should have a "How to Play" section with instructions on how to play the game.

8. The game should have a "High Score" feature to display the player's highest score achieved.