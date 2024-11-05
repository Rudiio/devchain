from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.exceptions import BadRequest

from user_manager import UserManager
from session_manager import SessionManager
from error_handler import ErrorHandler

class App:
    """
    The main application class that initializes the Flask app, configures routes,
    and runs the server. It uses UserManager and SessionManager to handle user
    registration, login, and session management, and ErrorHandler to manage errors.
    """

    def __init__(self):
        """
        Initialize the Flask application, configure session management, and set up routes.
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
        self.app.config['SESSION_TYPE'] = 'filesystem'
        Session(self.app)

        self.user_manager = UserManager()
        self.session_manager = SessionManager(self.app, session_timeout=900)  # 15 minutes timeout
        self.error_handler = ErrorHandler()

        self.configure_routes()

    def configure_routes(self):
        """
        Configure the URL routes for the application.
        """
        @self.app.route('/')
        def home():
            return redirect(url_for('login'))

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                
                try:
                    # Use UserManager to register user
                    user = self.user_manager.register_user(username, password, email)
                    flash('Registration successful! Please log in.', 'success')
                    return redirect(url_for('login'))
                except BadRequest as e:
                    flash(str(e), 'error')
            return render_template('register.html')

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                # Attempt to log in user
                if self.session_manager.login_user(username, password):
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password.', 'error')
            return render_template('login.html')

        @self.app.route('/dashboard')
        def dashboard():
            if 'logged_in' in session and session['logged_in']:
                return render_template('dashboard.html')
            return redirect(url_for('login'))

        @self.app.route('/logout')
        def logout():
            self.session_manager.logout_user()
            return redirect(url_for('login'))

        @self.app.route('/forgot_password', methods=['GET', 'POST'])
        def forgot_password():
            if request.method == 'POST':
                email = request.form['email']
                # Implement password reset logic here
                # This is a placeholder for the actual password reset logic
                # which should involve generating a password reset token,
                # sending an email to the user, and allowing the user to reset
                # their password using the token.
                flash('Password reset instructions have been sent to your email.', 'info')
            return render_template('forgot_password.html')

    def run(self):
        """
        Run the Flask application.
        """
        self.app.run(debug=True)

# Entry point for the application
if __name__ == '__main__':
    app = App()
    app.run()
