# error_handler.py

class ErrorHandler:
    """
    Handles error reporting and user notifications without exposing sensitive information or system details.
    This class is used across the application to provide secure and informative error messages to the user.
    """

    @staticmethod
    def handle_login_error():
        """
        Returns a generic error message for login failures to avoid revealing sensitive information.
        
        :return: A string containing the error message for login failures.
        """
        return "Invalid username or password. Please try again."

    @staticmethod
    def handle_registration_error():
        """
        Returns a generic error message for registration failures to avoid revealing sensitive information.
        
        :return: A string containing the error message for registration failures.
        """
        return "Registration failed. Please check the provided details and try again."

    @staticmethod
    def handle_reset_password_error():
        """
        Returns a generic error message for password reset failures to avoid revealing sensitive information.
        
        :return: A string containing the error message for password reset failures.
        """
        return "Password reset failed. Please check the provided details and try again."
