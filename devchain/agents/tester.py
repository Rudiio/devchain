import json
from colorama import Fore, Style

from rich.console import Console

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.prompts.tester import write_tests_stack, design_tests, write_test_file_list, write_tests_task, refine_tests_task
from devchain.communication.document import Document
from devchain.utils.io import pop_save_json

console = Console()

class Tester(Agent):
    """Tester agent class. Its main goal is to create the tests for the produced software.
    He takes as an input the code previously checked by the 
    """
    
    job : str = "Tester"
    target_document : str = "Tests"
    role : str = """You are a professional quality assurance engineer in a software developpement team."""
    goals: str = """Your goal is to design and write structured and maintainable tests and testcases for softwares."""
    memory_bool : bool = True
    
    def decide_and_act(self,)->Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        # Logic branch to design the tests
        if self.working_message.object=='Code_to_test' and self.working_message.origin_agent=='Developer':
           doc = Document.to_code(self.working_dir)
           return self.design_tests(name=doc.title,
                                   user_stories=doc.user_stories,
                                   requirements=doc.requirements,
                                   class_diagram=doc.class_diagram,
                                   stack=doc.stack,
                                   front=doc.front)
        
        # Logic branch to write the tests
        if self.working_message.object=='Tests_to_write' and self.working_message.origin_agent=='Tech_lead':
           plan = Document.load_plan(path=f'{self.working_dir}/misc/test_plan.json')
           return self.tests_writting_session(plan=plan)
    
        if self.working_message.object=='Tests_to_debug' and self.working_message.origin_agent=='Developer':
            fixes = Document.load_fixes(path=f'{self.working_dir}/misc/test_fixes.json')
            return self.tests_refining_session(fixes=fixes)
    
    def design_tests(self,
                     name:str,
                     user_stories:str,
                     requirements:str,
                     class_diagram:str,
                     stack:str,
                     front:str)->Message:
        """Design the tests to help writting the tests afterward. 
        It consists in identifying the features that should be tested, choosing the technology and listing the files to write"""
        
        print(Fore.GREEN + f'==> {self.__class__.__name__} is designing the tests [powered by {self.llm.model_name}]')
        
        # Choosing the tech stack
        with console.status(f'[bold green]{self.__class__.__name__} is choosing the testing stack [powered by {self.llm.model_name}]'):
            mission = write_tests_stack.format(name=name,
                                               stack=stack)
            test_stack = Document.parser.parse_code(self.execute(mission=mission,context=''))
        
        # Design the testcases
        with console.status(f'[bold green]{self.__class__.__name__} is designing the testcases [powered by {self.llm.model_name}]'):
            mission = design_tests.format(name=name,
                                          user_stories=user_stories,
                                          requirements=requirements,
                                          class_diagram=class_diagram,
                                          stack=stack,
                                          front=front)
            tests_design = self.execute(mission=mission,context='')
        
        # Write the file list
        with console.status(f'[bold green]{self.__class__.__name__} is writting the file list [powered by {self.llm.model_name}]'):
            mission = write_test_file_list.format(name=name,
                                                  testcases=tests_design,
                                                  class_diagram=class_diagram,
                                                  stack=test_stack,
                                                  front=front)
            tests_file_list = self.execute(mission=mission,context='')
            
        Document.save_tests_design(working_dir=self.working_dir,
                                   test_stack=test_stack,
                                   testcases=tests_design,
                                   file_list=tests_file_list)
        
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_plan_tests'},file)
        
        return Message(object="Testing_to_plan",
                       target_agent="Tech_lead",
                       origin_agent="Tester")  
        
    def tests_writting_session(self,plan:list[dict])->Message:
        """Generate the tests for the produced software according to the testing plan"""
        
        print(Fore.GREEN + f'==> {self.__class__.__name__} is writting the tests [powered by {self.llm.model_name}]' + Style.RESET_ALL)
        shared_doc = Document.to_code(self.working_dir) 
        
        for n in range(len(plan)):
            task = plan[n]
            # Retrieve the code to modify
            legacy_tests = Document.load_file(f"{self.working_dir}/tests/{task['file']}")
            
            # Format the prompt
            mission = write_tests_task.format(name=shared_doc.title,
                                                class_diagram=shared_doc.class_diagram,
                                                files_description=shared_doc.file_description,
                                                file=task['file'],
                                                tests=legacy_tests,
                                                task_description=task['description'],
                                                task_technology=task['technology'],
                                                task_instructions=task['instructions'],
                                                task_needed=task['needed'],
                                                working_dir=self.working_dir.split('/')[-1],
                                                front=shared_doc.front)
            
            # Execute the task
            console.log(task)
            with console.status(f"[bold green]{self.__class__.__name__} is solving task #{task['id']} (total={plan[-1]['id']})"):
                tests = self.execute(mission=mission,verbose=True)
            
            # Saving the file
            Document.save_code(code=tests,path=f"{self.working_dir}/tests/{task['file']}")
            
            # Pop the task
            pop_save_json(field='tasks',iter=plan[n:],path=f'{self.working_dir}/misc/test_plan.json')
        
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_review'},file)
            
        return Message(object='Review',
                       target_agent='Senior_developer',
                       origin_agent='Tester',)
    
    def tests_refining_session(self,fixes:list[dict])->Message:
        """Refine the tests according to the fixes given by the senior developper"""
        
        print(Fore.GREEN + f'==> {self.__class__.__name__} is refining the tests [powered by {self.llm.model_name}]' + Style.RESET_ALL)
        shared_doc = Document.to_code(self.working_dir)
        
        for n in range(len(fixes)):
            fix = fixes[n]
            # Retrieve the code to modify
            legacy_tests = Document.load_file(f"{self.working_dir}/tests/{fix['file']}")
            
            # Format the prompt 
            mission = refine_tests_task.format(name=shared_doc.title,
                                               class_diagram=shared_doc.class_diagram,
                                               files_description=shared_doc.file_description,
                                               file=fix['file'],
                                               tests=legacy_tests,
                                               fix_description=fix['description'],
                                               fix_technology=fix['technology'],
                                               fix_issue=fix['issue'],
                                               fix_instructions=fix['instructions'],
                                               fix_needed=fix['needed'],
                                               working_dir=self.working_dir)
            
            # Retrieve the code context based on the dependencies
            code_context=''
            if self.rag.retriever is not None:
                if fix['needed'] !='None':
                    code_context = self.rag.invoke(str(fix['needed']))
                    
            # Execute the tasks
            console.log(fix)
            with console.status(f"[bold green]{self.__class__.__name__} is applying fix #{fix['id']} (total={fixes[-1]['id']})"):
                tests = self.execute(mission=mission,context=code_context)
            
            # Saving the code file in the right folder
            Document.save_code(path=f'{self.working_dir}/tests/{fix["file"]}',code=tests)
            
            # Pop the task
            if n==len(fixes)-1:
                iter = []
            else:
                iter = fixes[n+1:]
            pop_save_json(field='fixes',iter=iter,path=f'{self.working_dir}/misc/test_fixes.json')
            
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_review'},file)
            
        return Message(object='Review',
                       target_agent='Senior_developer',
                       origin_agent='Tester')