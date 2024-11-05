import os

class ConfigManager:
    def __init__(self):
        self.config = {}

    def load_config_from_file(self, file_path):
        """
        Loads configuration settings from a file.
        
        :param file_path: The path to the configuration file.
        """
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Check if the line contains an equal sign before processing
                    if '=' not in line:
                        print(f"Warning: Skipping line '{line.strip()}'. No equal sign found.")
                        continue
                    key, value = line.strip().split('=', 1)
                    self.config[key] = value
        except FileNotFoundError:
            print(f"Configuration file {file_path} not found.")
        except Exception as e:
            print(f"An error occurred while reading the configuration file: {e}")

    def load_config_from_env(self, env_var):
        """
        Loads configuration settings from an environment variable.
        
        :param env_var: The name of the environment variable.
        """
        env_config = os.getenv(env_var)
        if env_config:
            for item in env_config.split(';'):
                parts = item.strip().split('=')
                if len(parts) == 2:
                    key, value = parts
                    self.config[key] = value
                else:
                    print(f"Warning: Skipping incorrectly formatted item '{item}'. Expected format: KEY=VALUE")
        else:
            # Provide a default configuration or prompt the user to set the variable
            self.prompt_for_config(env_var)

    def prompt_for_config(self, env_var):
        """
        Prompts the user for configuration settings if the environment variable is not set.
        
        :param env_var: The name of the environment variable.
        """
        print(f"Environment variable {env_var} not set. Please provide the configuration.")
        print("Enter configuration settings in the format KEY=VALUE, separated by semicolons (;).")
        print("Example: GREETING_FORMAT=Hello, {name}!;ANOTHER_SETTING=value")
        user_input = input("Enter configuration: ")
        for item in user_input.split(';'):
            parts = item.strip().split('=')
            if len(parts) == 2:
                key, value = parts
                self.config[key] = value
            else:
                print(f"Warning: Skipping incorrectly formatted item '{item}'. Expected format: KEY=VALUE")
        # Optionally, you could also save the provided configuration to an environment variable
        os.environ[env_var] = user_input

    def determine_and_load_config(self, file_path, env_var):
        """
        Determines the source of the configuration and loads it accordingly.
        
        :param file_path: The path to the configuration file.
        :param env_var: The name of the environment variable.
        """
        if os.path.isfile(file_path):
            self.load_config_from_file(file_path)
        else:
            self.load_config_from_env(env_var)

    def get_config(self, key):
        """
        Retrieves the value for a given configuration key.
        
        :param key: The configuration key.
        :return: The configuration value or None if the key is not found.
        """
        return self.config.get(key)
