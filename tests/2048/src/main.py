import pygame
import sys
from game_board import GameBoard
from game_logic import GameLogic
from ui_manager import UIManager
from input_handler import InputHandler
from score_manager import ScoreManager

def initialize_game():
    score_manager = ScoreManager()
    game_board = GameBoard()
    game_logic = GameLogic(game_board, score_manager)
    ui_manager = UIManager(game_board, score_manager)
    input_handler = InputHandler(game_logic, ui_manager)

    # Reset the score when initializing the game
    score_manager.reset_score()

    game_logic.spawn_tile()
    game_logic.spawn_tile()

    return game_board, game_logic, ui_manager, input_handler, score_manager

def handle_state_transitions(game_logic, ui_manager, score_manager):
    if game_logic.check_win_condition():
        ui_manager.show_message("Congratulations, you've won! Press 'C' to continue or 'Q' to quit.")
        return 'won'
    elif game_logic.check_game_over():
        ui_manager.show_message('Game Over! Press "R" to restart or "Q" to quit.')
        return 'over'
    return 'continue'

def main_game_loop(game_board, game_logic, ui_manager, input_handler, score_manager):
    running = True
    state = 'continue'
    clock = pygame.time.Clock()
    while running:
        action = input_handler.handle_events()
        if action == 'exit':
            running = False
        elif action == 'restart' and state in ['won', 'over']:
            game_board, game_logic, ui_manager, input_handler, score_manager = initialize_game()
            state = 'continue'
        elif action in ['up', 'down', 'left', 'right']:
            move_valid, points = game_logic.perform_move(action)
            if move_valid:
                state = handle_state_transitions(game_logic, ui_manager, score_manager)
        # Removed the unnecessary 'continue' and 'won' state handling block
        elif action == 'quit':
            running = False

        ui_manager.update_ui()
        clock.tick(60)

if __name__ == '__main__':
    try:
        pygame.init()
        game_board, game_logic, ui_manager, input_handler, score_manager = initialize_game()
        main_game_loop(game_board, game_logic, ui_manager, input_handler, score_manager)
    except KeyboardInterrupt:
        print("Game has been interrupted.")
    finally:
        pygame.quit()
        sys.exit()
