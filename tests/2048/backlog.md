# Backlog

## Name
MergeMaster 2048

## User stories
1. As a player, I want to be able to start a new game so that I can play anytime I want.
    Acceptance criteria:
    - There should be a "New Game" button on the main screen.
    - Clicking the "New Game" button should start a fresh game with an initial 2 or 4 randomly placed on
the board.

2. As a player, I want to control the movement of the blocks using keyboard arrow keys or swipe gestures
so that I can play the game easily.
    Acceptance criteria:
    - Pressing the arrow keys or swiping on a touchscreen should move the blocks in the corresponding
direction.
    - The blocks should move as far as possible in the chosen direction until they hit the edge of the
board or another block.

3. As a player, I want similar numbered blocks to merge when they touch so that I can aim to reach the
2048 block.
    Acceptance criteria:
    - When two blocks with the same number touch, they should merge into one block with the sum of the
two numbers.
    - The merging of blocks should only occur once per move for each individual block.

4. As a player, I want a new block to appear randomly on the board after each valid move so that the
game can progress.
    Acceptance criteria:
    - After every valid move, a new block with a number 2 or 4 should appear in a random empty space on
the board.

5. As a player, I want to win the game when I create a block with the number 2048 so that I have a goal
to work towards.
    Acceptance criteria:
    - When a 2048 block is formed, the game should display a "You Win" message.
    - The player should have the option to continue playing after winning or to start a new game.

6. As a player, I want the game to end if there are no valid moves left so that I know when the game is
over.
    Acceptance criteria:
    - If the board is full and no adjacent blocks can be merged, the game should display a "Game Over"
message.
    - The "Game Over" message should include the player's final score and an option to start a new game.

7. As a player, I want to see my current score so that I can keep track of my progress.
    Acceptance criteria:
    - The current score should be displayed on the screen at all times during the game.
    - The score should increase by the sum of the numbers on the newly merged blocks after each move.

8. As a player, I want to be able to undo my last move so that I can correct mistakes.
    Acceptance criteria:
    - There should be an "Undo" button that allows the player to revert to the state before the last
move.
    - The "Undo" feature should be limited to one use per move.

## Requirements
1. The game should be implemented using a modern programming language suitable for game development,
such as JavaScript with HTML5 and CSS3 for web implementation.

2. The game board should be a 10x10 grid, and the UI should clearly represent the different numbered
blocks.

3. The game should have smooth animations for block movements and merging to enhance the user
experience.

4. The game should have a simple and intuitive user interface that is also visually appealing.

5. The game should be playable on both desktop and mobile devices, with support for keyboard and touch
inputs respectively.

6. The game should store the current game state locally to allow the player to resume the game if it is
closed or refreshed.

7. The game should have a scoring system that calculates the score based on the sum of the numbers on
the newly merged blocks.

8. The game should have sound effects for block movements, merging, and winning or losing the game, with
an option to mute the sounds.

9. The game should prevent invalid moves where no blocks would move or merge, and not spawn a new block
in such cases.

10. The game should include a tutorial or help section that explains the rules and controls to new
players.