import os
import json

from pydantic import BaseModel, Field

from rich.console import Console

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage
from devchain.communication.document import Document
from devchain.prompts.senior_developer import review_code,review_tests, select_files, review_fixes, select_context, parse_code_review
from devchain.tools.run_code import RunCode
from devchain.tools.run_tests import RunTests
from devchain.utils.io import ask_user_text
from devchain.utils.prints import print_agent_action

console = Console()

class SeniorDeveloper(Agent):
    """Developer agent class. Its main goal is to create the code for the software and save it into a file.
    He have three actions :
        - Installing the dependencies based on the stack selected by the software architect (via a tool).
        - Writting the code (via llm capabilities).
        - Running the code (via a tool).
        - Identifying the bugs and fixes.
    """
    
    job : str = "Senior developer"
    target_document : str = "Code reviews"
    role : str = """You are a senior software engineer in a software developpement team specialized in code review. You are strict in your reviews and very good at noticing bugs.
    Your first concern is to create a fully-functional application, so you don't preocupate too much on minor bugs and focus on making the application run correctly."""
    goals: str = """You provide insightful, useful code and tests reviews to make the aaplication functionnal. """
    memory_bool: str = False
    max_iterations : int = 3
    tools : dict[str,BaseModel] = Field(default={'RunCode':RunCode(),
                                                 'RunTests':RunTests()},
                                        description="Stores the tools for executing tests and code")
    
    async def decide_and_act(self,)->Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        if self.working_message.object=='Review' and self.working_message.origin_agent=='Tester':
            doc = Document.to_code_tests(self.working_dir)
            
            return await self.review(name=doc.title,
                               erd=doc.erd,
                               code_stack=doc.stack,
                               code_files_description=doc.roles,
                               test_stack=doc.testing_stack,
                               test_files_description=doc.test_files_description)
        
        if self.working_message.object=='Fixes_to_review' and self.working_message.origin_agent=="Senior_developer":
            doc = Document.to_code_tests(self.working_dir)
            
            # Test fixes
            if self.test_logic:
                self.review_fixes(name=doc.title,
                                  path=f'{self.working_dir}/misc/test_fixes.json',
                                  files=doc.test_files_description,)
            
            # Code fixes
            return await self.review_fixes(name=doc.title,
                                     path=f'{self.working_dir}/misc/test_fixes.json',
                                     files=doc.roles)
                                                              
    async def review(self,
               name:str,
               code_files_description:str,
               erd:str,
               code_stack:str,
               test_stack:str,
               test_files_description:str)->Message:
        """Make the agent execute the code and give a full review of the code and its execution"""
        
        print_agent_action(agent=self,action="is starting the reviews")
        
        # Running the application
        execution_output = await self.run_code(stack=code_stack)
        
        # Running the tests
        if self.test_logic:
            test_output = self.run_tests(test_stack=test_stack)
        else:
            test_output = ''
            
        # Get user feedback
        if self.is_connected():
            msg = WsMessage.create_msg(object='',
                                        action='chat',
                                        agent=self.job,
                                        msg_content="Please give your feedback on the application. If you are creating a web application, please add the logs from the console.",
                                        document='Review',
                                        model=self.llm.model_name)
            await self.websocket.send_json(data=msg)
            user_feedback = (await self.websocket.receive_json())['content']['content']
        else:
            user_feedback = await self.ask_user_feedback()
        
        # Selecting the files to review
        if self.test_logic:
            selected_files = self.select_file_to_review(name=name,
                                                        execution_output=execution_output,
                                                        test_output=test_output,
                                                        user_feedback=user_feedback,
                                                        code_files_description=code_files_description,
                                                        test_files_description=test_files_description)
        else:
            selected_files = await self.select_file_to_review(name=name,
                                                        execution_output=execution_output,
                                                        test_output='',
                                                        user_feedback=user_feedback,
                                                        code_files_description=code_files_description,
                                                        test_files_description='')
            
        
        # Removing legacy file
        if os.path.exists(path=f'{self.working_dir}/misc/fixes.json'):
            os.remove(f'{self.working_dir}/misc/fixes.json')

        fixes_waterfall = ''
        for file in selected_files:
            # Executing the task
            print_agent_action(self,action=f"is reviewing {file}")
            self.target_document = f"Code review : `{file}`"
            
            # Routing between code and tests
            # TODO : improve the test detection with regex 
            if file[:4]=='test' and self.test_logic:
                self.review_tests(name=name,
                                  file=file,
                                  execution_output=execution_output,
                                  test_output=test_output,
                                  files_description=code_files_description,
                                  fellow_fixes=fixes_waterfall,
                                  test_stack=test_stack)
            else:
                json_review,review = await self.review_code(name=name,
                                                      file=file,
                                                      erd=erd,
                                                      execution_output=execution_output,
                                                      test_output=test_output,
                                                      user_feedback=user_feedback,
                                                      fellow_fixes=fixes_waterfall,
                                                      files=code_files_description,
                                                      stack=code_stack)
                # Putting the fixes into a string
                try:
                    if len(json_review['fixes']>0):
                        fixes_waterfall += f"\n\n{json_review}"
                except TypeError:
                    fixes_waterfall += f"\n\n{review}"
        
        # The fixes need to be reviewed
        fixes = Document.load_fixes(path=f'{self.working_dir}/misc/fixes.json')
        test_fixes = Document.load_fixes(path=f'{self.working_dir}/misc/test_fixes.json')
        
        # Checking if there are some fixes to apply
        if len(fixes)>0 or (len(test_fixes)>0 and self.test_logic):
            with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_debug_code'},file)
            return Message(object='Fixes_to_review',
                    target_agent='Senior_developer',
                    origin_agent='Senior_developer')
        
        # The project is complete
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_end'},file)
                
        return Message(object='Project_completed',
                       target_agent='Product_owner',
                       origin_agent='Senior_developer')
        
    async def review_code(self,
                    name:str,
                    file:str,
                    erd:str,
                    execution_output:str,
                    test_output:str,
                    user_feedback:str,
                    fellow_fixes:str,
                    files:str,
                    stack:dict):
        """Review the code of the application"""
        
        # Exctracting the relevant code context
        code_context = await self.select_review_context(name=name,
                                                  file=file,
                                                  files=files,
                                                  erd=erd)
        
        # Loading the code
        code = Document.load_file(f"{self.working_dir}/src/{file}")
        
        with console.status(f'[bold green]{self.__class__.__name__} is reviewing {file} [powered by {self.llm.model_name}]'):
            mission = review_code.format(name=name,
                                         file=file,
                                         code=code,
                                         erd=erd,
                                         files=files,
                                         execution_output=execution_output,
                                         test_output=test_output,
                                         user_feedback=user_feedback,
                                         fellow_fixes=fellow_fixes,
                                         stack=stack)
            
            review = Document.parser.parse_code(await self.execute(mission=mission,context=code_context))
        
        with console.status(f'[bold green]{self.__class__.__name__} is parsing the review [powered by {self.llm.model_name}]'):
            mission = parse_code_review.format(name=name,
                                               erd=erd,
                                               files=files,
                                               fixes=review)
            review = await self.execute(mission=mission)
            
        # Parsing the file
        review = Document.parser.parse_code(review)
            
        # Saving the fixes
        Document.save_fixes(f'{self.working_dir}/misc/fixes.json',review)
        
        json_review = json.loads(review)
        
        return json_review,review
        
    def review_tests(self,
                     name:str,
                     file:str,
                     class_diagram:str,
                     execution_output:str,
                     test_output:str,
                     files_description:str,
                     fellow_fixes:str,
                     test_stack:dict,
                     front:str):
        """Review a test file of the application"""
        
        tests = Document.load_file(f"{self.working_dir}/tests/{file}")
        mission = review_tests.format(name=name,
                                      file=file,
                                      class_diagram=class_diagram,
                                      front=front,
                                      tests=tests,
                                      execution_output=execution_output,
                                      test_output=test_output,
                                      files_description=files_description,
                                      fellow_fixes=fellow_fixes,
                                      test_stack=test_stack)
       
        review = self.execute(mission=mission)
        
        # Parsing the file
        review = Document.parser.parse_code(review)
            
        # Saving the fixes
        Document.save_fixes(f'{self.working_dir}/misc/test_fixes.json',review)
        
    async def ask_user_feedback(self,)->str:
        """Ask for the user feedback about the application execution.
        Returns the inputed feedback"""
        
        message = f"{self.__class__.__name__} is asking : Please give me your feedback on the execution of the application."
        return await ask_user_text(message=message)
        
    async def select_file_to_review(self,
                              name:str,
                              execution_output:str,
                              test_output:str,
                              user_feedback:str,
                              code_files_description:str,
                              test_files_description)->list[str]:
        """ Make the LLm to choose the right files to review based on the executions and feedback"""
        
        print_agent_action(self,action="is selecting files")
        
        # Getting the LLM output
        mission = select_files.format(name=name,
                                      execution_output=execution_output,
                                      test_output=test_output,
                                      user_feedback=user_feedback,
                                      files=code_files_description,
                                      test_files_description=test_files_description)
        
        with console.status(f'[bold green]{self.__class__.__name__} is selecting the files to review [powered by {self.llm.model_name}]'):
            selected_files = Document.parser.parse_code( await self.execute(mission=mission,context='',
                                                                            prefix="Based on the provided, informations, the following files need to be reviewed.\n"))
        
        # Converting the string to list
        selected_files = Document.parser.parse_python_list(python_list=selected_files)
        
        return selected_files
    
    async def select_review_context(self,
                              name:str,
                              file:str,
                              files:str,
                              erd:str) -> str:
        """Allow the Senior dev to select the context that he need to review the file"""
        
        print_agent_action(self,action="is selecting the context")
        
        with console.status(f'[bold green]{self.__class__.__name__} is selecting the code context [powered by {self.llm.model_name}]'):
            mission = select_context.format(name=name,
                                            file=file,
                                            files=files,
                                            erd=erd,
                                            codebase=self.rag.dump())
            context_list = await self.execute(mission=mission, prefix=f"Here is the code context that I need to review `{file}`\n")
            
        context_list = Document.parser.parse_code(context_list)
        
        # Converting the string to list
        context_list = Document.parser.parse_python_list(context_list)
        
        # Retrieve the context
        if len(context_list)>0:
            return self.rag.invoke(context_list)
        return ''
          
    async def review_fixes(self,
                     name:str,
                     path:str,
                     files:str)->Message:
        """Review the fixes to ensure that they will solve the right issues on the right files. Also making sure that the dependencies are respected."""
    
        print_agent_action(agent=self,action="is adjusting the fixes")
        fixes = Document.load_file(f'{self.working_dir}/misc/fixes.json')
    
        mission = review_fixes.format(name=name,
                                      files=files,
                                      fixes=fixes)
        
        with console.status(f'[bold green]{self.__class__.__name__} is adjusting the fixes [powered by {self.llm.model_name}]'):
            fixes = await self.execute(mission=mission,context='')
        
        # Parsing the file
        fixes = Document.parser.parse_code(fixes)
            
        # Saving the fixes
        Document.save_fixes(path=path,new_fixes=fixes,overwrite=True)
        
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_debug_code'},file)
            
        return Message(object='Code_to_debug',
                    target_agent='Developer',
                    origin_agent='Senior_developer')
        
    async def run_code(self,stack:str)->str:
        """Run the code of the application and returns the output"""
        # Choose the tool
        tool = self.tools['RunCode']
        
        # Running the code
        execution_output = await tool(requirements=stack,
                                working_dir=self.working_dir,
                                websocket=self.websocket)
        
        execution_output = "```" + '\n'.join(execution_output) + "```"
        
        execution_output = "The app was executed, here is the output\n" + execution_output
        
        if self.is_connected():
            msg = await WsMessage.acreate_msg(object="Execution",
                                       action="processing",
                                       document='App execution',
                                       model='None',
                                       agent=self.job,
                                       msg_content=execution_output,
                                       streaming=False)
            await self.websocket.send_json(msg)
        else:
            print(execution_output)
        
        return execution_output
        
    def run_tests(self,test_stack:str='')->str:
        """Run the tests of the application"""        
        # Choose the tool
        tool = self.tools['RunTests']
        
        # Running the code
        test_output = tool(working_dir=self.working_dir,
                           requirements=test_stack)
        
        test_output = '\n'.join(test_output)
        
        print(test_output)
        
        return test_output
        
        
        
    
        