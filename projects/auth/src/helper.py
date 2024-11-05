import os
from werkzeug.security import generate_password_hash, check_password_hash

class Helper:
    """
    Helper class provides utility functions for password hashing, salting,
    and validation of user input.
    """

    @staticmethod
    def hash_password(password):
        """
        Hash a password for storing, using a salted hash.

        :param password: The password to hash.
        :return: A salted hash of the password.
        """
        # Generate a salt using the dedicated method
        salt = Helper.generate_password_salt()
        # Hash the password with the salt
        password_hash = generate_password_hash(password + salt)
        # Return the salt and hash together
        return salt + password_hash

    @staticmethod
    def check_password_hash(password_hash, password):
        """
        Check a password against a given salted hash.

        :param password_hash: The hash to check against.
        :param password: The password to check.
        :return: True if the password matches the hash, False otherwise.
        """
        # Extract the salt from the stored hash
        salt = password_hash[:32]  # Assuming the salt is the first 32 characters
        # Recreate the salted hash with the extracted salt and the provided password
        return check_password_hash(password_hash[32:], password + salt)

    @staticmethod
    def generate_password_salt():
        """
        Generate a random salt for password hashing.

        :return: A random salt.
        """
        # Generate a random salt and return its hexadecimal representation
        return os.urandom(16).hex()
