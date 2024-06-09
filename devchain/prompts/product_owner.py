write_backlog = \
""" 
You are starting the development of a new application for a client. Here the application that he requested : {request}.

**Instructions**:
Write the Complete and precise backlog (user stories, requirements) for the request of teh user.
1. Give all the user stories and requirements that are relevant.
2. Detail the response that you give.
3. Give the corresponding acceptance criteria.
4. Incorporate all the requirements and features from the user demand.
5. Find an original and imaginative name for the application
6. Don't propose to test the application in the backlog as it is already part of the process.

FOLLOW strictly this format:
# Backlog

## Name
name

## User stories
1. user story
    Acceptance criteria:
    - acceptance criterion
    
## Requirements
    - requirements    

FOLLOW strictly these example:

* example 1:
# Backlog

## Name
Snake Game

## User stories
1. As a player, I want to be able to control the snake's movement using the arrow keys.
    Acceptance criteria:
    - When I press the up arrow key, the snake should move upwards.
    - When I press the down arrow key, the snake should move downwards.
    - When I press the left arrow key, the snake should move to the left.
    - When I press the right arrow key, the snake should move to the right.

2. As a player, I want the snake to grow longer when it eats the food.
    Acceptance criteria:
    - When the snake's head collides with the food, the snake's length should increase by one segment.
    - The food should then appear in a new random position on the screen.

3. As a player, I want the game to end if the snake collides with the walls or itself.
    Acceptance criteria:
    - If the snake's head touches the game boundaries, the game should end and display the "Game Over" message.
    - If the snake's head collides with its own body, the game should end and display the "Game Over" message.

## Requirements
1. The game should be implemented in Python.

2. The game shoukd use pygame.

3. The snake's movement should be smooth and responsive to the arrow key inputs.

4. The game should have a graphical interface with visual representations of the snake, food, and game boundaries.

5. The game should keep track of the player's score, which increases each time the snake eats the food.

6. The game should have sound effects for actions such as eating the food and ending the game.

* example 2:
# Backlog

## Name
GitHub Repository Stats Web Application

## User stories
1. As a user, I want to enter the name of a GitHub repository and see its statistics.
    Acceptance criteria:
    - There should be an input field where I can type the name of a GitHub repository.
    - After entering the name and submitting, I should see the statistics of the repository.

2. As a user, I want to see the number of stars, forks, and open issues of a repository.
    Acceptance criteria:
    - The web application should display the number of stars the repository has.
    - The web application should display the number of forks the repository has.
    - The web application should display the number of open issues the repository has.

3. As a user, I want the web application to be visually appealing and easy to navigate.
    Acceptance criteria:
    - The web application should have a clean and modern user interface.
    - The layout should be intuitive, with clear indications of where to enter data and where to find the repository statistics.
4. As a user, I want the web application to be responsive so that I can view it on different devices.
    Acceptance criteria:
    - The web application should be usable on desktops, tablets, and mobile phones.
    - The layout should adjust to the size of the device's screen without losing functionality or aesthetic appeal.

## Requirements
1. The web application should be written in Python, with HTML and CSS code included directly inside the Python code using string templates.

2. The application should use the GitHub API to fetch repository statistics.

3.The application should have error handling for cases such as incorrect repository names or issues with the GitHub API.

4. The application should be hosted on a web server, making it accessible via a web browser.

5. The application should have a clear and concise README file with instructions on how to use it.

6. The application should be tested across different web browsers to ensure compatibility and responsiveness.

"""

write_new_features = """
You are working on an application named {name}.

The user is asking you to add these features into the application:
{new_features}

Here are the user stories that are already implemented into the actual software:
{legacy_user_stories}.

Here are the requirements that the applicaton is already taking into account:
{legacy_requirements}.

**Instructions**:
Write the Complete and precise backlog (user stories, requirements) that correspond to the new features asked by the user.
1. Give all the user stories and requirements that are relevant.
2. Don't give anything that is too broad : split and breakdown at maximum.
3. Detail the response that you give.
4. Give the corresponding acceptance criteria.
5. Incorporate all the requirements and features from the user demand.
6. Find an original and imaginative name for the application
7. Don't propose to test the application in the backlog as it is already part of the process.

FOLLOW strictly this format:
# Backlog

## Name
name

## User stories
1. user story
    Acceptance criteria:
    - acceptance criterion
    
## Requirements
    - requirements    

FOLLOW strictly these example:

* example 1:
# Backlog

## Name
Snake Game

## User stories
1. As a player, I want to be able to control the snake's movement using the arrow keys.
    Acceptance criteria:
    - When I press the up arrow key, the snake should move upwards.
    - When I press the down arrow key, the snake should move downwards.
    - When I press the left arrow key, the snake should move to the left.
    - When I press the right arrow key, the snake should move to the right.

2. As a player, I want the snake to grow longer when it eats the food.
    Acceptance criteria:
    - When the snake's head collides with the food, the snake's length should increase by one segment.
    - The food should then appear in a new random position on the screen.

3. As a player, I want the game to end if the snake collides with the walls or itself.
    Acceptance criteria:
    - If the snake's head touches the game boundaries, the game should end and display the "Game Over" message.
    - If the snake's head collides with its own body, the game should end and display the "Game Over" message.

## Requirements
1. The game should be implemented in Python using a suitable GUI library such as Pygame.

2. The snake's movement should be smooth and responsive to the arrow key inputs.

3. The game should have a graphical interface with visual representations of the snake, food, and game boundaries.

4. The game should keep track of the player's score, which increases each time the snake eats the food.

5. The game should have sound effects for actions such as eating the food and ending the game.

* example 2:
# Backlog

## Name
GitHub Repository Stats Web Application

## User stories
1. As a user, I want to enter the name of a GitHub repository and see its statistics.
    Acceptance criteria:
    - There should be an input field where I can type the name of a GitHub repository.
    - After entering the name and submitting, I should see the statistics of the repository.

2. As a user, I want to see the number of stars, forks, and open issues of a repository.
    Acceptance criteria:
    - The web application should display the number of stars the repository has.
    - The web application should display the number of forks the repository has.
    - The web application should display the number of open issues the repository has.

3. As a user, I want the web application to be visually appealing and easy to navigate.
    Acceptance criteria:
    - The web application should have a clean and modern user interface.
    - The layout should be intuitive, with clear indications of where to enter data and where to find the repository statistics.
4. As a user, I want the web application to be responsive so that I can view it on different devices.
    Acceptance criteria:
    - The web application should be usable on desktops, tablets, and mobile phones.
    - The layout should adjust to the size of the device's screen without losing functionality or aesthetic appeal.

## Requirements
1. The web application should be written in Python, with HTML and CSS code included directly inside the Python code using string templates.

2. The application should use the GitHub API to fetch repository statistics.

3.The application should have error handling for cases such as incorrect repository names or issues with the GitHub API.

4. The application should be hosted on a web server, making it accessible via a web browser.

5. The application should have a clear and concise README file with instructions on how to use it.

6. The application should be tested across different web browsers to ensure compatibility and responsiveness.
"""