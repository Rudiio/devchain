import os
import sys
import argparse
from config_manager import ConfigManager
from greeting_manager import GreetingManager
from cli_interface import CLIInterface

def parse_arguments():
    """
    Parses the command-line arguments provided by the user.
    
    :return: Parsed arguments.
    """
    cli_interface = CLIInterface()
    return cli_interface.parse_user_input()

def start_interaction_loop(config):
    """
    Starts the main interaction loop of the application.
    
    :param config: The configuration settings.
    """
    greeting_manager = GreetingManager(config)
    cli_interface = CLIInterface()

    # Check if a name was provided as a command-line argument
    args = parse_arguments()
    if args.name:
        greeting_manager.display_greeting(args.name)
    else:
        # No name provided, prompt the user for their name
        try:
            name = greeting_manager.prompt_user_for_name()
            if name is not None:
                greeting_manager.display_greeting(name)
        except KeyboardInterrupt:
            cli_interface.display_message('\nOperation cancelled by user. Exiting...')
            sys.exit(0)

def check_environment_variable(env_var):
    """
    Checks if the necessary environment variable is set.
    
    :param env_var: The name of the environment variable to check.
    :return: True if the environment variable is set, False otherwise.
    """
    if os.getenv(env_var) is None:
        print(f"Error: The environment variable '{env_var}' is not set.")
        sys.exit(1)
    return True

def main():
    """
    The main entry point of the application.
    """
    # Environment variable name
    env_var = 'PYHELLOWORLD_CONFIG'  # Replace with your actual environment variable

    # Check if the environment variable is set before loading configuration
    if check_environment_variable(env_var):
        # Load configuration settings
        config_manager = ConfigManager()
        config_file_path = 'config.txt'  # Replace with your actual config file path
        config_manager.determine_and_load_config(config_file_path, env_var)
        config = config_manager.config

        # Start the interaction loop
        try:
            start_interaction_loop(config)
        except KeyboardInterrupt:
            print('\nApplication interrupted. Exiting...')
            sys.exit(0)

if __name__ == '__main__':
    main()
