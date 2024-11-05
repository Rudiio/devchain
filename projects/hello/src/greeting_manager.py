# projects/hello/src/greeting_manager.py
import sys
from .cli_interface import CLIInterface  # Corrected relative import

class GreetingManager:
    def __init__(self, config):
        self.config = config
        self.cli_interface = CLIInterface()

    def prompt_user_for_name(self):
        """
        Prompts the user for their name using the CLIInterface.
        Handles KeyboardInterrupt to exit gracefully.
        
        :return: The name provided by the user or None if interrupted.
        """
        try:
            self.cli_interface.display_message("Please enter your name:")
            return input()
        except KeyboardInterrupt:
            self.cli_interface.display_message("\nGoodbye! Have a great day!")
            sys.exit(0)

    def display_greeting(self, name):
        """
        Displays a personalized greeting message using the CLIInterface.
        
        :param name: The name of the user to be greeted.
        """
        greeting_format = self.config.get('GREETING_FORMAT', 'Hello, {name}!')
        greeting_message = greeting_format.format(name=name)
        self.cli_interface.display_message(greeting_message)
