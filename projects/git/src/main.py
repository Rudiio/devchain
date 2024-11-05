from flask import Flask, request, render_template_string
import requests

# Initialize the Flask application
app = Flask(__name__)

# Define the base URL for the GitHub API
GITHUB_API_BASE_URL = "https://api.github.com/repos/"

# Define the HTML template with embedded CSS for the web application
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Repository Statistics</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f7f7f7; }
        .container { max-width: 600px; margin: 50px auto; padding: 20px; background: #fff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        input[type="text"] { width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        input[type="submit"] { padding: 10px 20px; border: none; border-radius: 4px; background: #007bff; color: #fff; cursor: pointer; }
        input[type="submit"]:hover { background: #0056b3; }
        .stats { margin-top: 20px; }
        .error { color: #ff0000; }
    </style>
</head>
<body>
    <div class="container">
        <h1>GitHub Repository Statistics</h1>
        <form method="POST" action="/">
            <input type="text" name="repo_name" placeholder="Enter repository name (e.g. octocat/Hello-World)" required>
            <input type="submit" value="Get Statistics">
        </form>
        {% if stats %}
        <div class="stats">
            <strong>Stars:</strong> {{ stats.stars }}<br>
            <strong>Forks:</strong> {{ stats.forks }}<br>
            <strong>Open Issues:</strong> {{ stats.open_issues }}
        </div>
        {% endif %}
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# Define the RepositoryStatistics class to store and format repository statistics
class RepositoryStatistics:
    def __init__(self, stars, forks, open_issues):
        self.stars = stars
        self.forks = forks
        self.open_issues = open_issues

    @staticmethod
    def from_json(json_data):
        return RepositoryStatistics(
            stars=json_data.get('stargazers_count'),
            forks=json_data.get('forks_count'),
            open_issues=json_data.get('open_issues_count')
        )

# Define the GitHubAPIInterface class to handle communication with the GitHub API
class GitHubAPIInterface:
    @staticmethod
    def get_repository_stats(repo_name):
        response = requests.get(f"{GITHUB_API_BASE_URL}{repo_name}")
        if response.status_code == 200:
            return RepositoryStatistics.from_json(response.json())
        else:
            raise ValueError("Repository not found or GitHub API error")

# Define the ErrorHandler class to manage application errors and API exceptions
class ErrorHandler:
    @staticmethod
    def handle_error(error):
        return str(error)

# Define the route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    stats = None
    error = None
    if request.method == 'POST':
        repo_name = request.form['repo_name']
        try:
            stats = GitHubAPIInterface.get_repository_stats(repo_name)
        except Exception as e:
            error = ErrorHandler.handle_error(e)
    return render_template_string(HTML_TEMPLATE, stats=stats, error=error)

# Start the Flask web server
if __name__ == '__main__':
    app.run(debug=True)