plan_code = \
"""
You are working on the coding plan for an application called {name}.

Create a detailed step-by-step plan to implement the application. Always consider the fact that the codebase is modular and that the different files/components/classes need to interact.

Rules : 
- Make clear the role of each file/function/class, what they should perform and with what other element they should be integrated.
- Describe extensively each step. Give all the details that you can.
- 1 step = one precise task.
- Breakdown each step at maximum : implement the content of each file with multiple steps.
- For each file, think of its interaction with the other files based on the ERD and integrate that into the tasks.

Here is a full description of the application :
{description}

Here are the technologies that will be used to implement the application:
```json
{stack}
```

Here is a complete description of the roles and requirements of the files/classes. Make sure to understand it to create a good plan.
{files}

**IMPORTANT**
The plan that you write should only concern the writting of the code, no structure creation, git repo initialization, no tests, no documentation, no packages installation, only pure code writting.


Follow that format :
```markdown
- step 1
    - instruction 1
    - instruction 2
    - instruction 3
- step 2
    - instruction 1
    - instruction 2
    - instruction 3
- step 3
    - instruction 1
    - instruction 2
    - instruction 3
```
"""

translate_plan_code = \
"""
You are working on the coding plan for an application called {name}.

You need to translate the high-level implementation plan into a precise tasks plan that integrates with the structure of the application (ERD, file roles).
1. Make sure to understand deeply the provided plan.
2. Order the task in a logical order of implementation depending on their dependencies.
3. Only 1 file to modify per task.
4. Give a concise, yet clear task description.
5. Give VERY DETAILED instructions that will guide the developer.

Here is the high-level plan that was written:
```markdown
{plan}
```

Here is the complete description of the files and the classes:
{files}

Here are the technologies that will be used to implement the application:
```json
{stack}
```

**IMPORTANT**
Put the files as they are written.

**IMPORTANT**
DON'T forget to implement the entrypoint of the application in the main, app or application file to launch the application.

Follow the format of this example:
```json
{{
    "tasks": [
        {{
            "id": 1,
            "file": "file1.py",
            "technology": "Python",
            "description": "description",
            "instructions": "task1",
        }},
        {{
            "id": 2,
            "file": "file2.py",
            "technology": "Python",
            "description": "description",
            "instructions": "task2",
        }},
        ]
}}
```

"""