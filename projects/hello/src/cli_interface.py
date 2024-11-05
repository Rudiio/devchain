import argparse
import sys

class CLIInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PyHelloWorld Application")
        self._setup_parser()

    def _setup_parser(self):
        """
        Sets up the argument parser with the options for the application.
        """
        self.parser.add_argument('-n', '--name', type=str, help='Your name to personalize the greeting.')
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    def display_help_info(self):
        """
        Displays the help information for the application.
        """
        self.parser.print_help()

    def parse_user_input(self):
        """
        Parses the user input and returns the arguments.
        If parsing fails, the help information is displayed and the application exits.
        """
        try:
            args = self.parser.parse_args()
            return args
        except argparse.ArgumentError as e:
            self.display_message(str(e))
            self.display_help_info()
            sys.exit(2)

    def display_message(self, message):
        """
        Outputs a message to the user.
        
        :param message: The message to be displayed.
        """
        print(message)

    def handle_keyboard_interrupt(self):
        """
        Handles the KeyboardInterrupt exception by displaying a message to the user
        and exiting the application.
        """
        self.display_message('\nOperation cancelled by user. Exiting...')
        sys.exit(0)
