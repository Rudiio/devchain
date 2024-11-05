import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Ensure the static directory structure is correct
static_dir = os.path.join(app.root_path, 'static')
js_dir = os.path.join(static_dir, 'js')
css_dir = os.path.join(static_dir, 'css')

# Create directories if they do not exist
os.makedirs(js_dir, exist_ok=True)
os.makedirs(css_dir, exist_ok=True)

# Check for the presence of required static files and create placeholders if necessary
required_js_files = ['registration.js', 'login.js', 'feedback.js']
required_css_files = ['style.css', 'bootstrap.min.css']

for js_file in required_js_files:
    file_path = os.path.join(js_dir, js_file)
    if not os.path.isfile(file_path):
        open(file_path, 'a').close()  # Create an empty file

for css_file in required_css_files:
    file_path = os.path.join(css_dir, css_file)
    if not os.path.isfile(file_path):
        open(file_path, 'a').close()  # Create an empty file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except OSError as e:
        if e.errno == 98:  # Errno 98 means address already in use
            print("Port 5000 is already in use. Trying an alternative port...")
            app.run(port=5001, debug=True)
        else:
            raise
