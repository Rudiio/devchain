# PyHelloWorld Application

Welcome to the PyHelloWorld application! This application provides a simple command-line interface to display personalized greeting messages.

## Prerequisites

Before running the application, you need to set an environment variable that the application uses to load its configuration.

### Environment Variable

The application requires the following environment variable to be set:

- `PYHELOWORLD_CONFIG`: This variable holds the configuration settings for the application. It should contain key-value pairs separated by semicolons (`;`). For example: `GREETING_FORMAT=Hello, {name}!;ANOTHER_SETTING=value`.

### Setting the Environment Variable

To set the environment variable on your system, follow the instructions for your operating system:

#### On Windows

1. Open the Start Search, type in "env", and choose "Edit the system environment variables".
2. In the System Properties window, click on the "Environment Variables..." button.
3. In the Environment Variables window, under the "User variables" or "System variables" section, click on the "New..." button to create a new environment variable.
4. Enter `PYHELLOWORLD_CONFIG` as the variable name and the configuration settings as the value.
5. Click OK and apply the changes.

#### On macOS and Linux

1. Open a terminal window.
2. Use the following command to set the environment variable for the current session:
   