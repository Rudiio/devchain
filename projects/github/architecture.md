# Architecture
## Stack
```yaml
backend:
    languages: python
    libraries:
        - flask
frontend:
    languages:
        - javascript
        - css
        - html
    libraries:
        javascript:
            - axios
        css:
            - bootstrap
        html: []
```

## File list
Based on the provided user stories, technical stack, and requirements, here is a list of code files that will be written by the development team for the CodeTrendz application:

- `/app.py`: This file is the entry point of the Flask application. It will initialize the Flask app and define the routes for the API endpoints that handle repository search and statistics retrieval.

- `/repository_stats.py`: This file contains the `RepositoryStats` class that interfaces with the GitHub API to fetch the statistics for a given repository. It will handle the logic for retrieving the number of stars, forks, watchers, and open issues.

- `/templates/index.html`: This HTML file serves as the main page of the application. It includes the search bar for inputting the GitHub repository name and placeholders for displaying the repository's statistics.

- `/static/js/main.js`: This JavaScript file contains the client-side logic for handling user interactions with the search bar and sending AJAX requests using axios to the Flask backend. It also updates the frontend with the received repository statistics.

- `/static/css/styles.css`: This CSS file provides the styling for the application's frontend, ensuring that the search bar and statistics are presented in a user-friendly and visually appealing manner. It will include custom styles as well as Bootstrap classes for responsive design.


## Roles
Based on the provided context, here is the detailed description of each file's role within the MergeMaster 2048 application, their relationships, and the technical stack:

* `/app.py`:
    - This is the entry point of the Flask application.
    - It initializes the Flask app and sets up the web server.
    - It defines the routes for the API endpoints that handle repository search and statistics retrieval.
    - It renders the HTML template and includes CSS and JavaScript files for the frontend.
    - It uses the `RepositoryStats` class from `/repository_stats.py` to fetch repository statistics when a search is performed.

* `/repository_stats.py`:
    - Contains the `RepositoryStats` class that interfaces with the GitHub API.
    - The class includes methods to fetch and process repository statistics such as stars, forks, watchers, and open issues.
    - It provides the data that is requested by the AJAX calls made from `/static/js/main.js`.
    - This class is instantiated and used within the `app.py` to serve the necessary data to the frontend.

* `/templates/index.html`:
    - Serves as the main page of the application.
    - Contains the search bar for inputting the GitHub repository name and placeholders for displaying the statistics.
    - It is rendered by `app.py` when the root URL of the application is accessed.
    - It includes the script `/static/js/main.js` and the stylesheet `/static/css/styles.css`.
    - The content of this file is directly manipulated by `/static/js/main.js` through DOM manipulation.

* `/static/js/main.js`:
    - Contains the client-side logic for the application.
    - Handles user interactions with the search bar.
    - Sends AJAX requests to the Flask backend (`app.py`) and updates the frontend with the received data.
    - Interacts with `/templates/index.html` to manipulate the DOM and display the repository statistics.
    - It receives data from the `RepositoryStats` class through the backend endpoints defined in `app.py`.

* `/static/css/styles.css`:
    - Provides custom styling for the application's frontend.
    - Defines the look and feel of the search bar and statistics display.
    - Ensures a responsive design that adapts to different screen sizes.
    - It is included in `/templates/index.html` to style the HTML elements.


The technical stack for MergeMaster 2048 consists of Python with the Flask framework for the backend, HTML, CSS, and JavaScript for the frontend, and Bootstrap for UI components. The application is designed to be modular, with clear separation of concerns, allowing for efficient implementation and ensuring the quality of the final product.

## Entity relationship diagram
Given the context and instructions provided, here is the detailed Entity Relationship Diagram (ERD) for the CodeTrendz application:

```mermaid
erDiagram
    "app.py" ||--|| "repository_stats.py" : uses
    "app.py" ||--|| "index.html" : renders
    "app.py" ||--|| "main.js" : includes
    "app.py" ||--|| "styles.css" : includes
    "app.py" ||--|| "bootstrap.min.css" : includes
    "app.py" ||--|| "bootstrap.min.js" : includes
    "repository_stats.py" ||--|| "main.js" : provides-data-to
    "main.js" ||--|| "index.html" : manipulates
    "styles.css" ||--|| "index.html" : styles
    "bootstrap.min.css" ||--|| "index.html" : styles
    "bootstrap.min.js" ||--|| "index.html" : enables-interactivity

    "app.py" {
        functions initialize
        functions define-routes
    }
    "repository_stats.py" {
        class RepositoryStats
    }
    "index.html" {
        element search-bar
        element statistics-display
        element search-button
    }
    "main.js" {
        functions handle-search
        functions send-ajax-request
        functions update-frontend
    }
    "styles.css" {
        style search-bar-style
        style statistics-display-style
        style responsive-design
```