write_stack = \
"""
You are writting the design for an application called : {title}.

Here are the user stories that the final application need to incorporate:
{user_stories}

The product owner setted up the following requirements for the application:
{requirements}

**Instructions**
Choose the technical stack for the application. Make your choice based on ease of implementation (keep it simple), effectiveness and efficiency.
1. If the requirements already specify some technologies, you need to choose them.
2. Prioritize using python with pygame or flask.
3. Separate the technologies for the front-end and the back-end when necessary.
4. You need to consider 2 levels : the programming language and the libraries.

**Important**
Format your answer in YAML. Don't add any comment or explanations.

Follow Strictly this format:
```yaml
backend:
    languages: python
    libraries:
        - pygame
frontend:
    languages:
        -   javascript
        -   css
        -   html
    libraries:
        javascript:
            - axios
        css:
            - tailwind
        html:
            - bootstrap
```

"""

write_file_list = \
"""
You are listing the files for an application called : {title}.

**Instructions**
List the code files that will be written by the development team, based on the specifications of the application.

Rules:
- Keep it simple : don't add too many files.
- Ensure that the files have a real utility.
- Regroup the BIG main features together, ex : one file for rendering, one main file, one file for a class etc...
- Detail the description of each file.

Here is the technical stack that will be used to build the application:
{stack}
Here are the user stories that the final application need to incorporate:
```markdown
{user_stories}
```

The product owner setted up the following requirements for the application:
```markdown
{requirements}
```

**IMPORTANT**
Don't write any code.

**IMPORTANT**
Consider only the necessary CODE files that will translate the user stories and requirements. No other ressources.

STRICTLY follow the format of the following examples:
- /main.py: This file is the entry point of the application. It initializes the game, handles the game loop, and processes
user input for starting a new game and moving tiles.
- /game_board.py: This file contains the GameBoard class that manages the game state, including the grid, tile placement,
and merging logic.
- /game_logic.py: This file defines the GameLogic class that handles the rules of the game, such as valid moves, random tile
generation, and checking for win or game over conditions.
- /ui_manager.py: This file includes the UIManager class that manages the user interface elements, such as drawing the game
board, score display, and "New Game", "You Win!", and "Game Over" messages.
- /animation_manager.py: This file contains the AnimationManager class that handles the animations for tile movements and
merges to ensure a smooth visual experience.
- /score_manager.py: This file defines the ScoreManager class that calculates and updates the current score based on the sum
of merged tiles after each valid move.
"""

write_erd = \
"""

You are writting the design for an application called : {title}.

**Instructions**
Write the detailed entity relationship diagram (ERD) that describe the architecture of the code files that are part of the application, and their relations.
The ERD should summarize the back and front end designs.

Rules to build the ERD:
- An entity represents a file of the application.
- An entity can contain either functions, either a class, but NEVER includes functions or variables in the classes.
- If it should include functions then insert 'functions function"
- Don't include any arguments to the functions.
- If an entity contains a class, it CANNOT contain anything else.
- Include the relationship between the files.
- For CSS, list the styles that need to be written.
- For HTML, list the HTMLelements that need to be written.

Here are the list of files that are part of the application:
{files}

Here are the user stories that the final application need to incorporate:
```markdown
{user_stories}
```

The product owner setted up the following requirements for the application:
```markdown
{requirements}
```

Follow these examples :
* exmaple 1
```mermaid
erDiagram
    "main.py" ||--|| "game_board.py" : initializes
    "main.py" ||--|| "game_logic.py" : utilizes
    "main.py" ||--|| "ui_manager.py" : interacts
    "main.py" ||--|| "ui_manager" : controls
    "main.py" ||--|| "score_manager.py" : updates
    "game_board.py" ||--|| "game_logic.py" : applies
    "game_board.py" ||--|| "ui_manager" : triggers
    "ui_manager.py" ||--|| "ui_manager" : uses
    "score_manager.py" }}|--|| "game_logic.py" : relies-on

    "main.py" {{
        functions functions
    }}
    "game_board.py" {{
        class GameBoard
    }}
    "game_logic.py" {{
        class GameLogic
    }}
    "ui_manager.py" {{
        class UIManager
    }}
    "ui_manager" {{
        class AnimationManager
    }}
    "score_manager.py" {{
        class ScoreManager
    }}
```

* example 2
```mermaid
erDiagram
    "app.py" ||--|| "index.html" : renders
    "app.py" ||--|| "calculator.js" : includes
    "app.py" ||--|| "calculator_ui.js" : includes
    "app.py" ||--|| "styles.css" : includes
    "calculator.js" ||--|| "calculator_ui.js" : interacts
    "calculator_ui.js" ||--|| "index.html" : manipulates
    "styles.css" ||--|| "index.html" : styles

    "app.py"  {{
        functions function
    }}
    "calculator.js" {{
        class Calculator
    }}
    "calculator_ui.js" {{
        class CalculatorUI
    }}
    "index.html" {{
        element button-digits
        element button-operations
        element button-clear
        element button-all-clear
        element button-parentheses
        element display-current-input
        element display-complete-expression
    }}
    "styles.css" {{
        style button-styles
        style display-styles
        style calculator-layout
    }}
```
"""

write_roles = \
"""

You are describing the role and the requirements of each element that will compose an application called MergeMaster 2048.

Describe clearly the role of each file, classes of the codebase based on their short description, their relationship and the technical stack.
For that, follow a chain-of-thought reasoning:
- Think the role of each component in the application.
- Based on the ERD, understand which one should interact and how.
- List the main features/operations of each file. Include the integration, instanciation of other elements of the project.

Here are the list of files that are part of the application:
{files}

Here are the user stories that the final application need to incorporate:
```markdown
{user_stories}
```

The product owner setted up the following requirements for the application:
```markdown
{requirements}
```

The interactions between the different files are described by this Entity Relationship Diagram (ERD):
{erd}

Follow this format:
```markdown
* `snake.py`:
    - represent the snake via the Snake class
    - should include methods to eat, grow and move.
    - should be integrated into `game.py` via the Game class

* `game.py`:
    - contain the Game class that manipulates all of the element of the game.
    - ...
    - it includes the Snake class by having an instance. It controls the snake and integrate it into the workflow.

* `templates/index.html`:
    - contain the html code for the home of the web application.
    - it include the script `/static/js/main.js` and the stylesheet `/static/styles/styles.css`
    - `/static/js/main.js` manipulate directly its content by manipulating the DOM.
    - It integrates the styles from `/static/styles/styles.css` to style the html elements.
```

"""