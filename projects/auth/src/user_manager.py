import re
from werkzeug.exceptions import BadRequest
from email_validator import validate_email, EmailNotValidError
from user import User
from helper import Helper

class UserManager:
    """
    Manages user-related operations, including user registration, password reset, and user validation.
    It uses the User class to create and manage user objects and the Helper class for password validation.
    """

    def __init__(self):
        """
        Initialize the UserManager with an empty dictionary to store users.
        """
        self.users = {}

    def register_user(self, username, password, email):
        """
        Register a new user with a username, password, and email.

        :param username: The username of the new user.
        :param password: The password of the new user.
        :param email: The email of the new user.
        :return: User object if registration is successful, otherwise raises an exception.
        """
        try:
            if self.find_user_by_username(username):
                raise BadRequest("Username already exists.")
            
            if not self.validate_username(username):
                raise BadRequest("Invalid username.")
            
            if not self.validate_password(password):
                raise BadRequest("Password does not meet the criteria.")
            
            if not self.validate_email(email):
                raise BadRequest("Invalid email address.")
            
            user = User(username, email)
            user.set_password(password)
            self.users[username] = user
            return user
        except BadRequest as e:
            # Log the error for debugging purposes
            print(f"Registration error: {e.description}")
            raise

    def find_user_by_username(self, username):
        """
        Find a user by their username.

        :param username: The username to search for.
        :return: User object if found, None otherwise.
        """
        return self.users.get(username)

    def reset_password(self, username, new_password):
        """
        Reset the password for a user.

        :param username: The username of the user.
        :param new_password: The new password for the user.
        :return: True if the password was reset successfully, False otherwise.
        """
        user = self.find_user_by_username(username)
        if user:
            user.set_password(new_password)
            return True
        return False

    def validate_username(self, username):
        """
        Validate the username to ensure it meets the application's criteria.

        :param username: The username to validate.
        :return: True if the username is valid, False otherwise.
        """
        return re.match("^[a-zA-Z0-9_.-]+$", username) is not None

    def validate_password(self, password):
        """
        Validate the password to ensure it meets the strong password criteria.

        :param password: The password to validate.
        :return: True if the password is strong, False otherwise.
        """
        if len(password) < 8:
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search("[_!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def validate_email(self, email):
        """
        Validate the email address to ensure it is in a valid format.

        :param email: The email to validate.
        :return: True if the email is valid, False otherwise.
        """
        try:
            # Use the email-validator library to validate the email
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
