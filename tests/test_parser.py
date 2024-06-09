from devchain.utils.parser import DocumentParser
from devchain.communication.document import Document

parser = DocumentParser()

def test_parse_headers1():
    doc = Document.load_file("tests/mock/architecture.md")
    parsed = parser.parse_headers(doc=doc,max_level=6)
    
    assert isinstance(parsed,dict)
    
    # Checking level 1 
    keys = list(parsed.keys())
    assert keys == ['Architecture_and_design']
    
    # Checking level 2 
    keys = set(parsed['Architecture_and_design'].keys())
    assert keys == set(['Stack_selection','Design','Class_diagram','Files_list','Common_interface'])
    
    # Checking level 3
    keys = set(parsed['Architecture_and_design']['Common_interface'].keys())
    assert keys == {'Routes','Variables_and_form', 'Dependencies', 'CSS_classes'}
    
def test_parse_headers2():
    doc = Document.load_file("tests/mock/reviews/review_game_board.md")
    parsed = parser.parse_headers(doc=doc,max_level=6)
    
    assert parsed['Review']['Issues'] == """1. The `test_move_blocks_down`, `test_move_blocks_left`, `test_move_blocks_right`, and `test_move_blocks_up` are failing due to an `IndexError`. This is caused by an incorrect list comprehension that does not account for the size of the grid when reversing the rows or columns for the 'down' and 'right' moves.
2. The `test_has_valid_moves` is failing because the test setup does not reflect a situation where no valid moves are possible.
3. The implementation does not handle the case where pressing a key does not result in a valid move.
4. The code does not include a mechanism to detect when a 2048 block is created, nor does it handle the win condition.
5. The code does not handle the game over condition when no valid moves are left."""

    assert parsed['Review']['Fixes'] == """1. Fix the `move_blocks` method to correctly handle the 'down' and 'right' moves without causing an `IndexError`. Here is a code snippet to correct that:
    ```python
    def move_blocks(self, direction):
        # ... [existing code before the if statement] ...
        if direction in ('up', 'down'):
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size)]
                # Filter out zeros after reversing for 'down' direction
                column = [value for value in (column[::-1] if direction == 'down' else column) if value != 0]
                original_column = list(column)
                merged_column, column_score = self.merge_blocks(column)
                # Fill with zeros to maintain grid size
                merged_column += [0] * (self.size - len(merged_column))
                if direction == 'down':
                    merged_column.reverse()
                for i in range(self.size):
                    self.grid[i][j] = merged_column[i]
                score += column_score
                if original_column != merged_column:
                    moved = True
        elif direction in ('left', 'right'):
            for i in range(self.size):
                row = [self.grid[i][j] for j in range(self.size)]
                # Filter out zeros after reversing for 'right' direction
                row = [value for value in (row[::-1] if direction == 'right' else row) if value != 0]
                original_row = list(row)
                merged_row, row_score = self.merge_blocks(row)
                # Fill with zeros to maintain grid size
                merged_row += [0] * (self.size - len(merged_row))
                if direction == 'right':
                    merged_row.reverse()
                self.grid[i] = merged_row
                score += row_score
                if original_row != merged_row:
                    moved = True
        # ... [existing code after the if statement] ...
    ```
2. Update the `test_has_valid_moves` to correctly test for a situation where no valid moves are possible:
    ```python
    def test_has_valid_moves(self):
        # ... [existing test code] ...
        # Set up a grid with no valid moves
        self.game_board.grid = [[2, 4, 2, 4],
                                [4, 2, 4, 2],
                                [2, 4, 2, 4],
                                [4, 2, 4, 2]]
        self.assertFalse(self.game_board.has_valid_moves())
    ```
3. Implement a check for valid moves before adding a new number and updating the score:
    ```python
    def move_blocks(self, direction):
        # ... [existing code before adding a new number] ...
        if moved:
            if self.has_valid_moves():
                self.add_new_number()
                self.game_manager.update_score(score)
            else:
                self.game_manager.end_game()
        # ... [existing code after adding a new number] ...
    ```
4. Implement a check for the win condition in the `merge_blocks` method:
    ```python
    def merge_blocks(self, line):
        # ... [existing code before returning new_line and score] ...
        if 2048 in new_line:
            self.game_manager.win_game()
        return new_line, score
    ```
5. Implement the `end_game` method in the `GameManager` class to handle the game over condition:
    ```python
    class GameManager:
        # ... [existing GameManager methods] ...
        def end_game(self):
            # Display game over message and offer to start a new game
            print("Game Over! No valid moves left.")
            # ... [code to offer a new game] ...
    ```"""
    print(parsed.keys())
    assert parsed['Tests_need_to_be_corrected?'] == 'True'
    assert parsed['Code_need_to_be_corrected?'] == 'True'

def test_parse_user_stories():
    doc = Document.load_file("tests/mock/backlog.md")
    parsed = parser.parse_headers(doc=doc)['Backlog']
    
    user_stories = parser.parse_ordered_list(parsed['User_stories'])
    us1 = """As a player, I want to be able to move the tiles in four directions - up, down, left, and right.
    Acceptance criteria:
    - When I press the up arrow key, the tiles should move upwards and merge if they have the same value.
    - When I press the down arrow key, the tiles should move downwards and merge if they have the same value.
    - When I press the left arrow key, the tiles should move to the left and merge if they have the same value.
    - When I press the right arrow key, the tiles should move to the right and merge if they have the same value."""
    us2 = """As a player, I want the game to end when there are no more valid moves.
    Acceptance criteria:
    - If there are no empty spaces and no adjacent tiles with the same value, the game should end and display the "Game Over" message."""
    us3 = """As a player, I want to reach the 2048 tile to win the game.
    Acceptance criteria:
    - When a tile with the value of 2048 is created, the player wins the game and a "You Win" message is displayed."""
    
    sanitize = lambda x : x.replace(' ','').replace('\n','') 
    assert sanitize(user_stories[0]) == sanitize(us1)
    assert sanitize(user_stories[1]) == sanitize(us2)
    assert sanitize(user_stories[2]) == sanitize(us3)

def test_parse_requirements():
    doc = Document.load_file("tests/mock/backlog.md")
    parsed = parser.parse_headers(doc=doc)['Backlog']
    
    sanitize = lambda x : x.replace(' ','').replace('\n','') 
    requirements = parser.parse_ordered_list(parsed['Requirements'])
    req = [
        'The game should be implemented in Python using the Pygame library for the graphical interface.',
        "The tiles' movement should be smooth and responsive to the arrow key inputs.",
        "The game should have a graphical interface with visual representations of the tiles and the game board.",
        "The game should keep track of the player's score, which increases each time two tiles are merged.",
        "The game should have a \"New Game\" button to start a new game after winning or losing.",
        "The game should have a \"Quit\" button to exit the game at any time.",
        "The game should have a \"How to Play\" section with instructions on how to play the game.",
        "The game should have a \"High Score\" feature to display the player's highest score achieved."
    ]
    req = [sanitize(x) for x in req]
    requirements = [sanitize(x) for x in requirements]
    assert requirements==req

def test_python_list_parser():
    """ Test the python list parser that is required for the Code Context retriever"""
    
    # Classical test
    string1 = "[ab,cd]"
    assert parser.parse_python_list(string1) == ['ab','cd']
    
    # Empty list test
    string2 = '[]'
    assert parser.parse_python_list(string2) == []
    
    # Test with spaces
    string3 = '[   file.py,    file2.py]'
    assert parser.parse_python_list(string3) == ['file.py','file2.py']
    
    # Test with special characters
    string4 = "['file.py',\"file2.py\"]"
    assert parser.parse_python_list(string4) == ['file.py','file2.py']
    