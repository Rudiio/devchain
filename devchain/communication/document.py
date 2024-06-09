import os
import json
import yaml
from typing import ClassVar, Union
from pydantic import BaseModel, Field
import re
from re import Pattern

from devchain.utils.parser import DocumentParser
from devchain.utils.io import save_file,clean_folder

class Document(BaseModel):
    """Represent a document produced by an agent. It can contain all the generated documents"""
    title : str = Field(default='',description='title of the developped application')
    user_request : str = Field(default='',description="request made by the user")
    user_stories : str = Field(default='',description="Contains the user stories of the sprint")
    description : str = Field(default='',description="Decription of the application that need to be developped")
    requirements : str = Field(default='',description="Contains the requirements of the current sprint")
    stack : dict = Field(default='',description="Contains the stack of the application")
    erd : str = Field(default='',description="Class diagram of the application")
    file_description : str = Field(default='',description="Description of the files")
    roles : str = Field(default='',description="Describe the role of each file/ class")
    code: dict[str,str] = Field(default={},description="Code written and separated per file")
    testing_stack: Union[dict,str] = Field(default=None,description="Tech stack that will be used to test the application")
    testcases : Union[dict,str] = Field(default=None,description="List of testcases to implement")
    test_files_description : str = Field(default=None,description="List of test files that will be written")
    
    parser : ClassVar[DocumentParser] = DocumentParser()
    re_us : ClassVar[Pattern] = re.compile("^\d+_user_story\.md")
    re_req : ClassVar[Pattern] = re.compile("^\d+_requirement\.md")
    
    @staticmethod
    def load_file(path)->str:
        """Load a file into a string"""
        try:
            with open(path,'r+') as file:
                return file.read()
        except FileNotFoundError:
            # print("File does not exist")
            return ""
    
    @classmethod
    def load_informations(cls,working_dir:str):
        """Load the global informations of the project directly from the corresponding file"""
        
        # Load the adocument
        infos =  cls.load_file(f'{working_dir}/infos.md')
        infos = cls.parser.parse_headers(doc=infos,max_level=4)['Project_Informations']
        
        doc = Document()
        
        # User request
        if 'Request' in infos.keys():
            doc.user_request = infos['Request'].replace('\n\n','')
        # Name
        if 'Name' in infos.keys():
            doc.title = infos['Name'].replace('\n\n','')
        else:
            doc.title = None
            
        # Project description
        if 'Description' in infos.keys():
            doc.description = infos['Description'].replace('\n\n','')
        else:
            doc.description = None
        
        return doc
    
    @classmethod
    def save_backlog(cls,backlog:str,working_dir:str)->None:
        """Save the generated within the right format.
        One file per user story and one file per requirement"""
        
        # Parsing the file via the parser "tree construction"
        parsed_backlog = cls.parser.parse_headers(doc=backlog)['Backlog']
        cls.save_informations(working_dir=working_dir,info={'Name': parsed_backlog['Name']})
        
        # Parsing the ordered lists
        try:
            user_stories = cls.parser.parse_ordered_list(parsed_backlog['User_stories'])
        except KeyError:
            user_stories = cls.parser.parse_ordered_list(parsed_backlog['User_Stories'])
            
        requirements = cls.parser.parse_ordered_list(parsed_backlog['Requirements'])
        
        # Clean the folder
        clean_folder(f'{working_dir}/backlog/'),
        clean_folder(f'{working_dir}/requirements')
        
        # Saving the files
        for i in range(len(user_stories)):
            save_file(user_stories[i],f'{working_dir}/backlog/{i+1}_user_story.md')
        for i in range(len(requirements)):
            save_file(requirements[i],f'{working_dir}/requirements/{i+1}_requirement.md')
    
    @classmethod
    def save_code(cls,code:str,path:str):
        """Save the code in a specific file"""
        parsed_code = cls.parser.parse_code(code)
        save_file(parsed_code,path)
        return path
    
    @staticmethod
    def save_fixes(path:str,new_fixes:str,overwrite:bool=False) -> str:
        """Save the code in a specific file"""
        
        # If the fixes json file already exist
        if os.path.exists(path) and not overwrite:
            # Loading the old file
            with open(path,'r+') as file:
                fixes = json.load(file)
            # Loading the new fixes
            new_fixes = json.loads(new_fixes)
            
            # Fusing the changes
            fixes['fixes'] += new_fixes['fixes']
            
            # Resetting the ids
            for i in range(len(fixes['fixes'])):
                fixes['fixes'][i]['id'] = i + 1
            
            # Saving the new file
            with open(path,'w+') as file:
                json.dump(fixes,file)
        else:
            # Creating the fixes file
            with open(path,'w+') as file:
                file.write(new_fixes)
    
    @classmethod
    def save_tests(cls,working_dir:str,tests:str,name:str) -> str:
        """Save the code in a specific file"""
        parsed_tests = cls.parser.parse_code(tests)
        save_file(parsed_tests,f'{working_dir}/tests/{name}')
        return f'{working_dir}/tests/{name}'
    
    @staticmethod
    def save_informations(working_dir:str,info:dict) -> str:
        """Save the project informations in the correspoding file"""
        path = f'{working_dir}/infos.md'
        
        # Creating the file
        if not os.path.exists(path):
            with open(path,'w+') as file:
                file.write('# Project Informations\n\n')
        
        # Appending the informations
        with open(path,'a') as file:
            key = list(info.keys())[0]
            file.write(f'## {key}\n{info[key]}\n\n')
    
    @staticmethod
    def save_architecture(working_dir:str,
                          stack:str,
                          file_list:str,
                          erd:str,
                          roles:str) -> None:
        """Saves the string generated by the software architect"""
        
        architecture = "# Architecture\n"
        
        # Adding the stack
        architecture += "## Stack\n"
        architecture += stack + '\n\n'
        
        # Adding the file list
        architecture += "## File list\n"
        architecture += file_list + '\n\n'
        
        # Adding the Roles
        architecture += "## Roles\n"
        architecture += roles + '\n\n'
        
        # Adding the ERD
        architecture += "## Entity relationship diagram\n"
        architecture += erd + '\n\n'
        
        save_file(string=architecture,path=f'{working_dir}/architecture.md')
    
    @staticmethod
    def save_tests_design(working_dir:str,
                          test_stack:str,
                          testcases:str,
                          file_list:str)->None:
        """Saves the strings generated by Tester for the design of the tests"""
        
        test_design = "# Testing design\n"
        
        # Adding the stack
        test_design += "## Stack\n"
        test_design += test_stack + '\n'
        
        # Adding the testcases
        test_design += "## Testcases\n"
        test_design += testcases + '\n'
        
        # Adding the file list
        test_design += "## File list\n"
        test_design += file_list + '\n\n'
        
        save_file(string=test_design,path=f"{working_dir}/testing_design.md")
            
    @classmethod
    def from_backlog(cls,working_dir):
        """Create a document instance by loading the backlog directly from the folders"""
        # Current sprint directory
        sprint_folder = working_dir + '/current_sprint/'
        files = os.listdir(sprint_folder)
        
        doc = Document.load_informations(working_dir=working_dir)
        
        # Filtering each category
        us = list(filter(cls.re_us.match,files))
        req = list(filter(cls.re_req.match,files))
        
        # Sorting the files
        us.sort()
        req.sort()
        
        # Adding the user stories
        for i in range(len(us)):
            with open(sprint_folder + us[i],'r') as file:
                doc.user_stories += f'{i+1}. ' + file.read() + '\n'
        
        # Adding the requirements
        for i in range(len(req)):
            with open(sprint_folder + req[i],'r') as file:
                doc.requirements += f'{i+1}. ' + file.read() + '\n'
        
        return doc
    
    @classmethod
    def from_done_backlog(cls,working_dir):
        """Create a document instance by loading the backlog directly from the folders"""
        # Current sprint directory
        sprint_folder = working_dir + '/done/'
        files = os.listdir(sprint_folder)
        
        doc = Document()

        # Loading the title 
        with open(f'{working_dir}/name.md','r') as file:
            doc.title = file.read()
        
        # Filtering each category
        us = list(filter(cls.re_us.match,files))
        req = list(filter(cls.re_req.match,files))
        
        # Sorting the files
        us.sort()
        req.sort()
        
        # Adding the user stories
        for i in range(len(us)):
            with open(sprint_folder + us[i],'r') as file:
                doc.user_stories += f'{i+1}. ' + file.read() + '\n'
        
        # Adding the requirements
        for i in range(len(req)):
            with open(sprint_folder + req[i],'r') as file:
                doc.requirements += f'{i+1}. ' + file.read() + '\n'
        
        return doc
    
    @classmethod
    def to_code(cls,working_dir:str):
        """Create a document instance by loading the backlog + code directly from the folders"""
        doc = cls.from_backlog(working_dir)
        
        # Load the architecture
        architecture =  cls.load_file(f'{working_dir}/architecture.md')
        try:
            architecture = cls.parser.parse_headers(doc=architecture)['Architecture']
        except KeyError:
            architecture = cls.parser.parse_headers(doc=architecture)['Architecture']
            
        # No need of processing : stack, design, class diagram
        keys = architecture.keys()
        
        if 'Stack' in keys:
            try:
                doc.stack = yaml.safe_load(cls.parser.parse_code(architecture['Stack']))
            except yaml.error.YAMLError:
                doc.stack = architecture['Stack']
            
        if 'Entity_relationship_diagram' in architecture:
            # Exctracting only the class diagram to prevent from hallucinations
            cls_diag = re.search("```mermaid.*```",flags=re.DOTALL,string=architecture['Entity_relationship_diagram'])
            doc.erd = cls_diag.group(0)
        
        if 'Roles' in architecture:
            doc.roles = architecture['Roles']
        
        # Need of processing : file list and file description
        to_parse = architecture['File_list']
        pattern_description = re.compile('((?:\*|\+|-)\s+.+)+$',re.DOTALL)
        doc.file_description = pattern_description.findall(to_parse)[0]
        
        return doc
    
    @classmethod
    def to_code_tests(cls,working_dir:str):
        """Create a document by loading the tests design and application architecture"""
        doc = cls.to_code(working_dir=working_dir)
        
        try:
            # Load the architecture
            test_design =  cls.load_file(f'{working_dir}/testing_design.md')
            try:
                test_design = cls.parser.parse_headers(doc=test_design)['Testing_design']
            except KeyError:
                print("Could not parse the testing design")
                
            # Adding the stack
            if 'Stack' in test_design:
                try:
                    doc.testing_stack = yaml.safe_load(test_design['Stack'])
                except yaml.error.YAMLError:
                    doc.testing_stack = test_design['Stack']
            
            # Adding the test cases
            if 'Testcases' in test_design:
                testcases = re.search("```json.*```",flags=re.DOTALL,string=test_design['Testcases']).group(0)
                try:
                    doc.testcases = json.loads(testcases)
                except json.JSONDecodeError:
                    doc.testcases = test_design['Testcases']

            # Adding the list of files
            if 'File_list' in test_design:
                pattern_description = re.compile('((?:\*|\+|-)\s+.+)+$',re.DOTALL)
                try:
                    doc.test_files_description = pattern_description.findall(test_design['File_list'])[0]
                except TypeError:
                    doc.test_files_description = test_design['File_list']
        except TypeError:
            pass
        
        return doc
    
    @staticmethod
    def sanitize_needed(string:str)->str:
        """Sanitize the needed field of a task/fix to make it respect the format awaited by the Code_context_retriever."""
        # Remove the spaces
        string = string.replace(' ','')
        
        # if needed is a single str
        if isinstance(string,str):
            string = string.replace('\n','').replace('[','').replace(']','')
            parsed = string.split(',')
            
            # Handling str : single answer or list of answers
            if len(parsed)==1:
                if len(parsed[0])>2:
                    string = [string]
                else:
                    return []
            else:
                string = string.split(',')
                
        return string        
    
    @classmethod
    def load_plan(cls,path:str)->list[dict]:
        """Load the plan from directly from /misc/plan.json"""
        
        # Unfortunately load an str
        with open(path,'r+') as file:
            plan = json.load(file)
        
        return plan['tasks']
    
    @classmethod
    def load_fixes(cls,path:str)->list[dict]:
        """Load a fix file"""
        # Load into a dict
        if os.path.exists(path):
            with open(path,'r+') as file:
                fixes = json.load(file)
            
            return fixes['fixes']
        else:
            return []

        
        
        
        
        

        
        
    
    
