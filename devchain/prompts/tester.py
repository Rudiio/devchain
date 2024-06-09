design_tests=\
"""
You are working on an application named `{name}` and you need to design the tests of the application.

Here are the user stories that the final application need to incorporate:
{user_stories}

The product owner setted up the following requirements for the application:
{requirements}

Keep in my that the game was developed with the following technologies, so adapt your test design to it:
{stack}

This class diagram is the base for the backend of the application and should help you when coding:
{class_diagram}
Important : When writting the code, refer to this class diagram when it makes sense for the task.

The software architect created this design for the front-end of the application:
{front}

**Instructions**
Identify precisely based on all the informations, the features and the cases that should be tested in the application. 
1. Make sure that you cover all the edge cases.
2. Ensure that the tests allow to spot potential bugs or broken features that don't appears clearly in the code.
3. Use the class diagram to understand the architecture of the application.
4. Give also with each case, the way to test it.
Don't test the front-end.

**IMPORTANT**
Don't tests the non-functional requirements, such as interactivity or responsiveness or resource usage.

**IMPORTANT**
Don't write more than 5 testcases, so focus on the main features.

**VERY IMPORTANT**
The goal of the tests is to verify the correctness of the implementation and to identify the flaws to the main features, so create the testcases with that in mind.

Respect this format:
```json
{{
    "testcases":[
        {{
            "id":1,
            "feature": verify that the snake is able to eat correctly the food and grow.,
            "how": put the snake on the food position and call the functions.
        }}
    ]
}}

"""

write_tests_stack=\
"""
You are working on an application named `{name}` and you need to design the tests of the application.

Here is the actual stack of the application:
{stack}

**Instruction**
Choose the stack that will be used to test the application. Make your choice based on ease of implementation (keep it simple), effectiveness and efficiency.
Priviledge using pytest for python testing.
Don't test the front-end.

**Important**
Format your answer in YAML. Don't add any comment or explanations.

Follow this example:
```yaml
Language: Python
Libraries:
    - pygame
```
"""

write_test_file_list = \
"""
You are working on an application named `{name}` and you need to design the tests of the application.

You already wrote the following testcases for the application:
{testcases}

And here is the stack that will be used to test the application:
{stack}

This class diagram is the base for the backend of the application and should help you when coding:
{class_diagram}
Important : When writting the code, refer to this class diagram when it makes sense for the task.

The software architect created this design for the front-end of the application:
{front}

**Instructions**
Based on the informations, list the test files that should be written for the application.
1. Regroup the test cases together per big features.
2. Choose a correct amount of files : not too much, not too less.
3. Describe the role of each file and the features and testcases that should be tested inside.
Don't test the front-end.

Follow STRICLTY the format of this example:
- `test_pi_estimation_precision.py`: This file will test the core functionality of Pi estimation, ensuring that the application can provide an estimate of Pi with various levels of precision as specified by the user (test cases 1, 2, 5).
- `test_pi_estimator_methods.py`: This file will focus on testing the methods of the PiEstimator class, including the ability to return the correct data types for estimates and descriptions, and the functionality of the reset method (test cases 11, 12, 13).
- `test_gui_elements.py`: This file will test all aspects of the GUI, including the intuitiveness and ease of navigation, the precision input validation, the calculate button's functionality, the result label updates, and the info button's behavior (test cases 6, 7, 8, 9, 10).
- `test_application_behavior.py`: This file will test the overall behavior of the application, including the ability to handle multiple estimations, error handling for invalid inputs, and resource usage during the estimation process (test cases 3, 4, 14, 15).
"""

write_tests_task = \
"""
You are working on an application named `{name}` and you are writting the tests for it.

Here is the class diagram of the application that express the architecture of the application.:
{class_diagram}

Here is the description of the code files that are part of the application:
{files_description}

You will be rewritting this file : `{file}`, here is the actual code in it:
```
{tests}
```

You need to solve this precise task by completing the code given above.
**Here is a description of the task**: {task_description}.
**You need to use this technology to solve the task** : {task_technology}
**Follow these instructions**: {task_instructions}.
**Take these functions or classes in account when implementing**: {task_needed}.

The code given in context is directly taken from the other files of the project, use them to understand how to use the methods that you need if they are present.

**IMPORTANT**
The code files are located in the `src` folder, so make the right import.

**IMPORTANT**
Rewrite entirely the given tests and add the modification asked by the task.

**IMPORTANT**
Rely heavily on the class diagram when access the classes, methods and attributes when writting the tests.

**IMPORTANT** Coding principles
Write high-quality code with qualitative comments. Aim for simplicity and adhere to DRY (Don't Repeat Yourself) principle to avoid code duplication.

Follow this format:
```
{{tests}}
```
"""

refine_tests_task = \
"""
You are working on an application named `{name}` and you are correcting the tests for it.

Here is the class diagram of the application that express the architecture of the application.:
{class_diagram}

Here is the description of the code files that are part of the application:
{files_description}

You will be rewritting this file : `{file}`, here is the actual code in it:
```
{tests}
```

You need to apply a precise fix to the code given below.
**Here is a description of the fix**: {fix_description}.
**technology** : {fix_technology}.
**Here is the issue that the fix need to solve** : {fix_issue}.
**Follow these instructions**: {fix_instructions}.
**Take these functions or classes in account when implementing**:{fix_needed}. Remember that they are implemented in the files listed below so don't reimplement them.

The code given in context is directly taken from the other files of the project, use them to understand how to use the methods that you need if they are present.

**IMPORTANT**
The code files are located in the `src` folder, so make the right import.

**IMPORTANT**
Rely heavily on the class diagram when access the classes, methods and attributes when writting the tests.

**IMPORTANT** Coding principles
Write high-quality code with qualitative comments. Aim for simplicity and adhere to DRY (Don't Repeat Yourself) principle to avoid code duplication.

Follow this format:
```
tests
```
"""

debug_tests = \
"""
You are working on an application called : {title} and you need to rewrite the tests so they can be functionning.

Here are the features that the application need to posses to meet the clients expectations:
{user_stories}
The tests need to verify them.

The application need to meet these requirements: 
{requirements}

Here is the code that the tests need to cover:
```
{code}
```

Here are the tests that need to be rewritten:
```
{buggy_tests}
```

Here are the files contained in the project.
{file_list}

Here is the code review given by the Senior developper, understand it deeply before fixing your tests.
### Issues
{issues}

### Fixes
{fixes}

**Instructions**:
Rewrite and correct the tests, based on the tests reviews so they can meet the user stories and requirements.
1. Write exhaustive tests cases for the code.
2. Make sure to test the main features of the software proposed into the user stories.
3. REMEMBER that the code is located into this folder `./{working_dir}/src/{file}`, so make the right imports.
5. If a method/function is difficult to test, DON'T test it.
5. VERIFY THAT YOUR TESTS ARE CORRECT.
7. FOCUS on the functionnalities, AVOID the tests that launch any GUI.
"""