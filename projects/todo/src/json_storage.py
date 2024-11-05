import json
import os

class JsonStorage:

    def __init__(self, file_path):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # Check if the file exists
        if not os.path.isfile(self.file_path):
            # If the file does not exist, create it with an empty list
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def read_tasks(self):
        try:
            with open(self.file_path, 'r') as file:
                tasks = json.load(file)
            return tasks
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist.")
            return []
        except json.JSONDecodeError:
            print(f"The file {self.file_path} is not a valid JSON file.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def write_tasks(self, tasks):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(tasks, file, indent=4)
        except IOError as e:
            print(f"An I/O error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
