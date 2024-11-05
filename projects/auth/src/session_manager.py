from flask import session, flash, redirect, url_for
from helper import Helper  # Import the Helper class
from user_manager import UserManager

class SessionManager:
    """
    Manages user sessions, including login, logout, and session timeout features.
    It interacts with the UserManager class to validate user credentials during login.
    """

    def __init__(self, app, session_timeout):
        """
        Initialize the SessionManager with the Flask app and session timeout value.

        :param app: The Flask application instance.
        :param session_timeout: The timeout value for user sessions in seconds.
        """
        self.app = app
        self.session_timeout = session_timeout
        self.user_manager = UserManager()

    def login_user(self, username, password):
        """
        Log in a user by checking their username and password.

        :param username: The username of the user attempting to log in.
        :param password: The password provided by the user.
        :return: True if login is successful, False otherwise.
        """
        user = self.user_manager.find_user_by_username(username)
        if user and Helper.check_password_hash(user.password_hash, password):
            session['user_id'] = user.username
            session['logged_in'] = True
            session.permanent = True
            self.app.permanent_session_lifetime = self.session_timeout
            return True
        else:
            flash('Invalid username or password.', 'error')
            return False

    def logout_user(self):
        """
        Log out the current user by clearing their session.
        """
        session.pop('user_id', None)
        session.pop('logged_in', None)
        return redirect(url_for('login'))

    def handle_session_timeout(self):
        """
        Handle the session timeout by logging out the user and redirecting to the login page.
        """
        flash('Your session has expired. Please log in again.', 'info')
        return self.logout_user()
