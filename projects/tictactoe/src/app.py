import pygame
import sys
from game import Game
from player import Player
from pygame_renderer import PygameRenderer
from symbol import Symbol
from game_status import GameStatus

def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    width, height = 300, 300

    # Create the screen surface
    screen = pygame.display.set_mode((width, height))

    # Initialize players
    player1 = Player("Player 1", Symbol.X)
    player2 = Player("Player 2", Symbol.O)

    # Initialize game
    game = Game(player1, player2)

    # Initialize PygameRenderer with the game instance
    renderer = PygameRenderer(game)

    # Start the game
    game.start_game()

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()
    fps = 30  # Desired frames per second

    # Main game loop
    running = True
    while running:
        # Handle events (user input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.get_game_status() == GameStatus.IN_PROGRESS:
                    x, y = pygame.mouse.get_pos()  # Corrected function call
                    row = y // (height // 3)
                    col = x // (width // 3)
                    if game.make_move(row, col):
                        renderer.render()
                else:
                    # Handle the case where the game is over
                    # Restart the game if the user clicks the screen
                    game.start_game()
                    renderer.render()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(fps)

        # Check game status and handle the end of the game
        if game.get_game_status() != GameStatus.IN_PROGRESS:
            # Render the final game state before displaying the result
            renderer.render()

            # Delay and display the game result before quitting
            pygame.time.wait(2000)  # Wait for 2 seconds
            screen.fill((0, 0, 0))  # Clear the screen

            # Create a font object
            font = pygame.font.Font(None, 36)

            # Determine the game result message
            if game.get_game_status() == GameStatus.X_WON:
                message = "Player 1 (X) wins!"
            elif game.get_game_status() == GameStatus.O_WON:
                message = "Player 2 (O) wins!"
            elif game.get_game_status() == GameStatus.DRAW:
                message = "It's a draw!"
            else:
                message = "Game over!"

            # Render the message
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)

            # Update the display
            pygame.display.flip()

            # Wait for a user action to either restart the game or quit
            waiting_for_action = True
            while waiting_for_action:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_action = False
                    elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        # Restart the game if the user clicks the screen or presses a key
                        waiting_for_action = False

            # Set running to False to exit the main loop after the game ends
            running = False

    # Corrected part: Added pygame.quit() after the main loop ends
    pygame.quit()

if __name__ == "__main__":
    main()
