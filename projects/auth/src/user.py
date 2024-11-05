from helper import Helper

class User:
    """
    Represents a user and handles user-related data and operations such as setting
    and checking passwords. This class relies on the Helper class for password management.
    """
    
    def __init__(self, username, email):
        """
        Initialize a new user with a username and email.

        :param username: The username of the user.
        :param email: The email of the user.
        """
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):
        """
        Set the password for the user by creating a hashed version.

        :param password: The password to hash and set for the user.
        """
        # Use the Helper class to hash the password
        self.password_hash = Helper.hash_password(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        :param password: The password to check.
        :return: True if the password matches the hash, False otherwise.
        """
        # Use the Helper class to check the password hash
        return Helper.check_password_hash(self.password_hash, password)
