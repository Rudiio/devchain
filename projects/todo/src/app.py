from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from werkzeug.exceptions import NotFound
from task_manager import TaskManager
from api_routes import api_blueprint

app = Flask(__name__, static_url_path='', static_folder='static')
task_manager = TaskManager()

# Register the Blueprint correctly with the Flask application instance
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def home():
    tasks = task_manager.get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/x-icon')
    except NotFound:
        # If favicon.ico is not found, you can choose to send a default icon or return a 404 error
        # Option 1: Send a default icon (assuming default_favicon.ico exists in the static directory)
        # return send_from_directory(os.path.join(app.root_path, 'static'),
        #                            'default_favicon.ico', mimetype='image/x-icon')
        # Option 2: Return a 404 error
        return jsonify({'message': 'Favicon not found'}), 404

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api'):
        return jsonify({'message': 'Resource not found'}), 404
    else:
        # Render the new '404.html' template with a user-friendly error message and a link to the home page
        return render_template('404.html', error_message='The page you are looking for cannot be found.', home_url='/'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api'):
        return jsonify({'message': 'Internal server error'}), 500
    else:
        return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
