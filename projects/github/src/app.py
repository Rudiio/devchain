from flask import Flask, render_template, request, jsonify
import requests
from repository_stats import RepositoryStats

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page of the application
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Extract the repository name from the request data
    data = request.json
    repository_name = data.get('repository_name')
    
    # Validate the repository name input
    if not repository_name:
        return jsonify({'error': 'Repository name is required'}), 400
    
    # Fetch repository statistics using the RepositoryStats class
    repo_stats = RepositoryStats(repository_name)
    stats = repo_stats.fetch_repository_data()
    
    # Check if statistics were successfully fetched
    if stats:
        return jsonify(stats)
    else:
        return jsonify({'error': 'Failed to fetch data for the specified repository'}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
