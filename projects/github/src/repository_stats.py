import requests

class RepositoryStats:
    def __init__(self, repository_name):
        self.repository_name = repository_name
        self.api_url = f"https://api.github.com/repos/{self.repository_name}"

    def get_stats(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            stats = {
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'watchers': data.get('watchers_count', 0),
                'open_issues': data.get('open_issues_count', 0)
            }
            return stats
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {}

    # Renamed method to match the one used in app.py
    def fetch_repository_data(self):
        return self.get_stats()
