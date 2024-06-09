# projects/2048/src/input_handler.py
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_r, K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT

class InputHandler:
    def __init__(self, game_logic, ui_manager):
        self.game_logic = game_logic
        self.ui_manager = ui_manager

    def handle_events(self):
        # Process all events from the event queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Handle key down events
                action = self.translate_input_to_action(event.key)
                if action:
                    # Return the action determined by the user's input
                    return action
            elif event.type == QUIT:
                return 'quit'
        return None

    def translate_input_to_action(self, event_key):
        # Map the Pygame key event to a game action (direction)
        key_action_mapping = {
            K_UP: 'up',
            K_DOWN: 'down',
            K_LEFT: 'left',
            K_RIGHT: 'right',
            K_ESCAPE: 'quit',
            K_r: 'restart',
            K_q: 'quit'
        }
        return key_action_mapping.get(event_key, None)

    # Additional function to test input handling
    def test_input_handling(self):
        # Simulate key presses for testing purposes
        test_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_r, K_q]
        key_action_mapping = {
            K_UP: 'up',
            K_DOWN: 'down',
            K_LEFT: 'left',
            K_RIGHT: 'right',
            K_ESCAPE: 'quit',
            K_r: 'restart',
            K_q: 'quit'
        }
        for key in test_keys:
            action = self.translate_input_to_action(key)
            assert action == key_action_mapping[key], f"Key {key} does not map to the correct action {action}."

        print("All key-action mappings are correct.")

# This function is not part of the class, but is used to run the test
def run_input_handler_test():
    # Mock objects for game_logic and ui_manager
    game_logic = type('MockGameLogic', (object,), {})()
    ui_manager = type('MockUIManager', (object,), {})()

    # Initialize InputHandler with mock objects
    input_handler = InputHandler(game_logic, ui_manager)
    # Run the test
    input_handler.test_input_handling()

# Uncomment the following line to run the test outside of the game loop
# run_input_handler_test()
