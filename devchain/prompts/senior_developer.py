review_code = \
"""
You are working on an application called {name} and you need to review a part of the code.

**Instructions**:
You have to review the code from `{file}` and list the fixes that need to be applied. Use all the information provided.
Read carefully the errors, code and feedback to identify the problems, here are some points that you should check:
1. If the code logic in `{file}` is correct.
2. If the code is fully implemented : verify that it does not contain any placeholders.
3. If the imports are made correctly in python and that the CDNs are present in the HTML code.
4. If the code is syntactically correct.
5. If the code from `{file}` is correctly used in the other files.

Rules:
- Focus on making the application work in its actual state.
- You can only propose to modify the code of the application, no command or other.
- Give a complete description of how to solve the issue.
- Take into account as much as possible that the fixes can affect other files, and create fixes for them.
- Use the code give in context to understand how the code that you need to review is used in the app.
- Assign each fix with the right file.
- If an issue if positive, then don't add it into the list.

You need to review this code from `{file}`:
```
{code}
```

You also need to consider that these fixes were already identified for the application's code:
{fellow_fixes}

Here is a description of the files that are part of the application and their precise role:
{files}

Here are the tests outputs. If it is empty then don't them that in account:
```
{execution_output}
```

The application can use ONLY these technologies:
{stack}

The user executed the program and here is its feedback, take it into account when it is not empty:
`{user_feedback}` 

**IMPORTANT**
List the issues and fixes using the markdown syntax.

```markdown
- issue 1
    - fix 1
    - fix 2
    - fix 3
- issue 2
    - fix 1
    - fix 2
    - fix 3
```

"""

parse_code_review = \
"""
Parse all the given fixes into the format that is indicated at the end.
1. Make sure to understand clearly the fixes to fill correctly the fields.
2. Make sure that the fixes correspond to the right file.
3. Order the task in a logical order of implementation depending on their dependencies.
4. Only 1 file to modify per task.
5. Give a concise, yet clear task description.
6. Give VERY DETAILED instructions that will guide the developer.

These are the fixes that you need to parse:
```markdown
{fixes}
```

Here is a description of the files that are part of the application and their precise role:
{files}

**IMPORTANT**
If there are no fixes, return an empty list in json format.

Follow strictly the format of this example:
```json
{{
    "fixes": [
        {{
            "id": 1,
            "file": "file.py",
            "technology": "Python",
            "issue" : "issue1"
            "description": "description",
            "instructions": "Instructions",
        }},
        {{
            "id": 2,
            "file": "file2.py",
            "technology": "Python, pygame",
            "issue" : "issue2"
            "description": "description",
            "instructions": "instructionss"
        }}
    ]
}}
```
"""

select_files = \
"""
You are working on an application called {name} and you need to review the code that is already written.

**Instructions**
Select the file that should be reviewed and corrected to make the application functional.

**Rules**
- Select only ONE or ZERO file.
- If everything is working fine, don't select anything and output an empty list.
- Respect the format given below.

Here is the list of code files with a quick description for each:
```markdown
{files}
```

The code of the application was executed and here is the output of its execution:
```
{execution_output}
```

The user followed the program execution and here is its feedback, take it into account:
{user_feedback}

**IMPORTANT**
Give the file name as they are given above.

**VERY IMPORTANT**
Follow STRICTLY the format of examples:
* example 1
```python
[setting.py]
```
* example 2
```python
[file.js]
```
* example 3
```python
[]
```
"""

select_context = \
"""
You need to select the code that you will need to see to review `{file}`.
To make you choice, you need to analyze carefully the relationships between the files in the ERD and the role of each file/class.
If some code is related then you need to select it.

You can ONLY select codes (files, classes or functions) that are mentionned here:
```
{codebase}
```

This is the descriptions of the roles and interactions of the files:
{files}

This File relationship diagram represents the global architecture of the project:
{erd}

**IMPORTANT**
Output the result in a python list. If there is no context, then output an empty list.

Rules:
- Don't select anything from `{file}`.
- You can select the code from a file, a class or a function.
- Return an empty list if no context should be selected.
- ONLY output the list.

Follow this format:
```
[file::class_name,file,file::class_name,file]
```
"""

review_tests = \
"""
You are working on an application called {name} and you need to review the tests that were already written. 

This class diagram represent the architeture of the backend of the application.
{class_diagram}

The following informations represent the front-end architecture of the application:
{front}

The following code are the tests that the testser from your team wrote for `{file}`:
```
{tests}
```

The code of the application was executed and here is the output of its execution:
```
{execution_output}
```

The application was also tested, here are the outputs of the tests:
```
{test_output}
```

Here are the files that constitute the application:
{files_description}

Here are the technologies that the tests can use:
{test_stack}

You already reviewed other CODE files of the application, here are the fixes that you proposed for them : 
{fellow_fixes}.
You need to take them into account in your actual review to not propose any redundent fixes if something is related to the actual file.

**Instructions**:
You have to review the tests from `{file}` and give the fixes that should be applied to correct it. Use all the information provided.
Your task consist in identifying the precise issues and giving specific solutions to them.
Here are the point that you should check:
1. If the tests are correct in term of code and code syntax.
2. If the tests are in agreelment with the architecture of the application.
2. If the tests are correct in term of pure features testing. 

Give enough information in the fixes description to guide the tester solving the problem.
You need to provide the precise functions or code portion that are needed from the other files to solve the task based on the given informations.

**IMPORTANT**
If the code is correct then return an empty list.

Follow strictly the format of this example:
```json
{{
    "fixes": [
        {{
            "id": 1,
            "file": "app.py",
            "technology": "Python",
            "issue" : "The application does not start"
            "description": "The application entrypoint is not implemented.",
            "instructions": "Implement the application entrypoint : 
            if __name__=='__main__':
                app = App()
                app.run()",
            "needed": "None"
        }},
        {{
            "id": 2,
            "file": "renderer.py",
            "technology": "Python, pygame",
            "issue" : "The game cannot render the cells"
            "description": "The `render_cell` function is missing from the code.",
            "instructions": "Implement the `render_cell` function in the `Renderer` class",
            "needed": "None"
        }},
        {{
            "id": 3,
            "file": "renderer.py",
            "technology": "Python, pygame",
            "issue": "Missing 'render_cell' method",
            "description": "The Renderer class is missing the 'render_cell' method which is causing an AttributeError when trying to call this method from the Application class.",
            "instructions": "Implement the 'render_cell' method in the Renderer class to draw the state of a cell at a given (x, y) position.",
            "needed": [
                {{"GitHubApiClient.get_star_history()": "Retrieve star history data for a given repository."}},
                {{"ErrorHandler.display_api_error()": "Display error message if API call fails."}}
            ]
        }},
        {{
            "id": 4,
            "file": "renderer.py",
            "technology": "Python, pygame",
            "issue": "Method 'visualize_cell_state' should be 'render_cell'",
            "description": "The Renderer class has a method named 'visualize_cell_state' which should be 'render_cell' according to the class diagram.",
            "instructions": "Rename the 'visualize_cell_state' method to 'render_cell' in the Renderer class to match the class diagram and to resolve the AttributeError.",
            "needed": "StarEvolutionGraph.update_graph()"
        }},  
    ]
}}
```

"""

review_fixes = \
"""
You are working on an application called {name} and you need to review the fixes that you made to correct the codebase of the application.

**Instructions**
Review the provided fixes and correct them if necessary..
1. Make sure that the selected file in the json is corresponding to the instructions of the fix.
2. Make sure that the fix is logical and clear enough.
3. Verify that the fixes are not redundent and remove any "duplicate".
4. Correct the fixes ids to have a real sequence.

Here is a description of the files that are part of the application and their roles:
{files}

Here are the fixes that you need to review:
{fixes}

**Important**
Give your answer in the exact same format as the input fixes.

Follow strictly the format of this example:
```json
{{
    "fixes": [
        {{
            "id": 1,
            "file": "file.py",
            "technology": "Python",
            "issue" : "issue1"
            "description": "description",
            "instructions": "Instructions"
        }},
        {{
            "id": 2,
            "file": "file2.py",
            "technology": "Python, pygame",
            "issue" : "issue2"
            "description": "description",
            "instructions": "instructionss"
        }}
    ]
}}
```
```
"""

