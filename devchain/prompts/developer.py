write_code_task = \
"""
**VERY VERY IMPORTANT** 
REWRITE the whole code as it was and modyfy the part that should be modified accordingly to the task. 
DO NOT shorten the code with any comment. 

You are working on an application called `{name}` and you need to write code for a part of the application.

You need to solve this precise task by rewritting the code given below, using the provided informations.
**Here is a description of the task**: {task_description}

**You need to use this technology to solve the task** : {task_technology}

**Follow these instructions**: {task_instructions}
Implement everything that is necessary to solve the task (additional functions), the goal is that everything is functionnal so implement everything that is needed even if it is not clearly said.

Use the code that is provided in context to help you to code correctly : use the correct functions and interfaces.

You will be rewritting this file : `{file}`, here is the actual code in it:
```
{code}
```

Remember that the code you will write is part of a bigger project that contains these files:
```markdown
{files}
```

**VERY IMPORTANT**
Write the content of every functions : don't let anything be a placeholder.

**IMPORTANT** Coding principles
- Write high-quality code with clear comments.
- Aim for simplicity and adhere to DRY (Don't Repeat Yourself) principle to avoid code duplication. 
- Make sure that the code that you write is coherent with the existing codebase shown in context.
- In Html, add the scripts in the body section and the stylesheets in the head section.
- Make sure to make the right imports in python scripts.
- For any javascript or CSS library use CDN to import them : there is no bundler available.
- For any javascript or CSS library that you use, make sure to add the correct CDN in the HTML code.

**IMPORTANT**
Don't give anything more than pure code.

Follow the following example:
```
code
```
"""

refine_code_task = \
"""
**VERY VERY IMPORTANT** 
REWRITE the whole code as it was and modyfy the part that should be modified accordingly to the task. 
DO NOT shorten the code with any comment. You can only modify THIS file : `{file}`.

You are working on an application called `{name}` and you need to correct a part of the code of the application.

You need to apply a precise fix to the code to correct the issue by using the provided informations.
**Here is a description of the fix**: {fix_description}

**You need to use that technology** : {fix_technology}

**Here is the issue that the fix will solve** : {fix_issue}

**Follow these instructions**: {fix_instructions}
Implement everything that is necessary to sove the task (additional functions), the goal is that everything is functionnal so implement everything that is needed even if it is not clearly said.

Use the code that is provided in context to help you to code correctly : use the correct functions and interfaces.

You will be rewritting this file : `{file}`, here is the actual code in it:
```
{code}
```

Remember that the code you will write is part of a bigger project that contains these files:
```markdown
{files}
```

**VERY IMPORTANT**
Write the content of every functions : don't let anything be a placeholder.

**IMPORTANT** Coding principles
- Write high-quality code with clear comments.
- Aim for simplicity and adhere to DRY (Don't Repeat Yourself) principle to avoid code duplication. 
- Make sure that the code that you write is coherent with the existing codebase shown in context.
- In Html, add the scripts in the body section and the stylesheets in the head section.
- Make sure to make the right imports in python scripts.
- For any javascript or CSS library use CDN to import them : there is no bundler available.
- For any javascript or CSS library that you use, make sure to add the correct CDN in the HTML code.

**IMPORTANT** Coding principles
Don't give anything more than pure code. Don't forget to import any module or library that you use.

Follow the following format:
```
code
```
"""

select_code_context = \
"""
You need to select the code that you will need to see to write code for `{task_file}`.
To make you choice, you need to analyze carefully the task's instructions and the role of each file/class.
If some code is related then you need to select it.

You can ONLY select codes (files, classes or functions) that are mentionned in the following codebase:
```
{codebase}
```

Here is the instructions of the task that will be treated:
{task_instructions}

This is the descriptions of the roles and interactions of the files:
{files}

**IMPORTANT**
You need to use the same exact files (and path) and class names that are mentioned in the codebase.

Rules:
- Don't select anything from `{task_file}`.
- You can select the code from a file, a class or a function.
- Return an empty list if no context should be selected.
- ONLY output the list.

Follow this format:
```
[file::class_name,file,file::class_name,file]
```

"""
