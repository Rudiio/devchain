import os
import questionary
from pathlib import Path
import shutil
import subprocess
import importlib
import json

async def ask_user_request()-> str:
    """Ask the user to send a request"""

    message = "What application do you want to develop ?"
    examples = [
        'Github statistics web application in python using flask. The front end should use html and CSS with tailwind.',
        'Snake game in python using pygame.',
        'Fibonacci calculator in python using dynamic programming.',
        'Tic tac toe game.',
        'Wave equation solver in python with numpy and matplotlib.',
        'Efficient Pi estimator.'
    ]
    response = questionary.autocomplete(message=message,
                             choices=examples,
                             qmark='==>',
                             ).ask_async()
    return response

def ask_user_question(question:str)->str:
    """Ask the user a question"""
    return questionary.text(message=question,
                             qmark='==>').ask()
                        
def ask_user_choice(message:str,choices)-> str:
    """Ask the user for a choise with a select questionary"""
    return questionary.select(message=message,
                       choices=choices,
                       qmark='==>').ask()

async def ask_user_choice_async(message:str,choices)-> str:
    """Ask the user for a choise with a select questionary"""
    return await questionary.select(message=message,
                       choices=choices,
                       qmark='==>').ask_async()
    
def ask_user_text(message)->str:
    """Ask the user to give a textual answer"""
    return questionary.text(message=message,
                            qmark='==>').ask()    

def str_to_markdown(string : str, path:str='', filename:str='') -> None:
    """"""
    try:
        with open(path + f"/{filename}.md",'w+') as file:
            file.write(rf'{string}')
            
    except ValueError as err:
        print(f"error : {err}")

def save_file(string:str,path:str) -> None:
    """Save a string into a file. Useful especially for code"""
    try:
        file = Path(path)
        file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path,'w+') as file:
            file.write(string)
            
    except ValueError as err:
        print(f"error : {err}")

def pop_save_json(field:str,iter:list[dict],path:str):
    """Pop the first element and then save the list into a new json"""
    dictionary = {field:iter}
    with open(path,'w+') as file:
        json.dump(dictionary,fp=file)
    
def create_folder(path:str) -> None:
    """ Create a folder if it does not exist"""
    if not os.path.exists(path):
            os.mkdir(path)

def create_file(path:str,overwrite:bool=False) -> None:
    """Create a new file."""
    if  os.path.exists(path):
        if overwrite:
            os.remove(path)
            open(path,'+w').close()
    else:
        open(path,'+w').close()

def clean_folder(path:str)->None:
    """Deletes all the files inside a folder"""
    
    for file in os.listdir(path):
            if os.path.exists(f'{path}/{file}'):
                # Removing directories
                if os.path.isdir(f'{path}/{file}'):
                    shutil.rmtree(f'{path}/{file}')
                else:   
                    os.remove(f'{path}/{file}')

def handle_requirements(requirements:dict)->None:
    """Handle the requirements : check if they are installer if not install them"""
    try:
        # Identify the programming language
        if 'Language' in requirements:
            programming_language = requirements['Language'].lower()
        else:
            programming_language = None
            
        # Identify the libraries to install
        if 'Libraries' in requirements:
            to_install = requirements['Libraries']
        else:
            to_install = None
        
        # For python
        if programming_language=='python':
            # Checking if the library are installed
            try:
                for module in to_install:
                    importlib.import_module(module)
                print("[Log] Libraries are already installed")
                
            except ImportError:
                print("[Log] Installing Library")
                for package in to_install:
                    subprocess.run(['pip','install',package],)
    except TypeError:
        print("Error when trying to install the dependencies")
def identify_programming_language(extension):
    if extension=='py':
        return 'python'