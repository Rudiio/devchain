import os
import shutil
import json
from rich.console import Console

from colorama import Fore, Style

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage
from devchain.communication.document import Document
from devchain.prompts.project_manager import write_project_description
from devchain.utils.io import ask_user_choice_async
from devchain.utils.prints import print_agent_action

console = Console()

class ProjectManager(Agent):
    """ 
    Project Manager agent class. Its main goal is to take inputs from the user and interact with him. He also makes a short descrition of the application.
    """
    job : str = "Project manager"
    target_document : str = "Project description"
    role : str = "You are the project manager and CTO, you have both technica and management skills. Your main goal is to plan the project implementation and breakdown the code writting into multiple steps."
    goals: str = "Breakdown the implementation process and plan into many substeps(tickets) that will be executed by the developer."
    streaming : bool = True
        
    async def decide_and_act(self) -> Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        if self.working_message is None:
            return ValueError("Communication error")

        # Need to write the product backlog if the message is the user input
        if self.working_message.object=='Product_backlog_to_plan' and self.working_message.origin_agent=="Product_owner":
            return await self.plan_sprint()

        # Wait any user user modification on the architecture
        if self.working_message.object=='Software_design' and self.working_message.origin_agent=="Software_architect":
            return await self.wait_modification(document='software design')
        
        # Plan the cycles
        if self.working_message.object=='Software_design' and self.working_message.origin_agent=='Project_manager':
            return self.plan_smaller_cycle()
        
    async def plan_sprint(self,) -> Message:
        """Plan the next sprint depending on the user."""
        print_agent_action(self,'is launching the sprint planning')
        status = True
        
        # Delete the previous current sprint
        # clean_folder(f'{self.working_dir}/current_sprint/')
        
        # Drag and drop loop
        while status:
            instructions = \
            """Please select the user stories and requirement that you want for the next sprint.
Drag the one that you want from their respective folder to the `current_sprint` folder.
`backlog/n_user_story` ==> `current_sprint
`requirements/n_requirement` ==> `current_sprint`"""

            # Questionary event
            if self.is_connected():
                msg = WsMessage.create_msg(object='',
                                           action='choice',
                                           agent=self.job,
                                           msg_content=instructions + "\nAre you done?",
                                           document='Sprint planning',
                                           model=self.llm.model_name,
                                           msg_sub_content=['Yes','No','All'])
                await self.websocket.send_json(data=msg)
                user_answer = (await self.websocket.receive_json())['content']['content']
                
            else:
                print(instructions)
                message = f"{self.__class__.__name__} is asking : Are you done ?" 
                user_answer = await ask_user_choice_async(message=message,
                                            choices=['Yes',
                                                    'No',
                                                    'All'])

            # Lazy response to copy everything
            if user_answer == 'All':
                dir = os.listdir(f'{self.working_dir}/backlog/')
                for file in dir:
                    shutil.move(f'{self.working_dir}/backlog/' + file,f'{self.working_dir}/current_sprint/')
                
                dir = os.listdir(f'{self.working_dir}/requirements/')
                for file in dir:
                    shutil.move(f'{self.working_dir}/requirements/' + file,f'{self.working_dir}/current_sprint/')
                status=False
            
            # Done
            if user_answer == 'Yes':
                status = False
            
        
        # Showing the current sprint backlog
        backlog = Document.from_backlog(working_dir=self.working_dir)
        sprint_backlog = f"""==> Planning is done, Here is the current backlog
        ## User stories
        {backlog.user_stories}
        
        ## Requirements 
        {backlog.requirements}"""
        
        print(sprint_backlog)
        
        print_agent_action(self,action='is describing the app')
        # Generating the application description
        with console.status(f'[bold green]{self.__class__.__name__} is writting the project description [powered by {self.llm.model_name}]'):
            description = await self.execute(mission=write_project_description.format(name=backlog.title,
                                                                                user_stories=backlog.user_stories,
                                                                                requirements=backlog.requirements),
                                       verbose=True)
            
        Document.save_informations(working_dir=self.working_dir,
                                   info={'Description':description})
        
        # Saving the state
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_design',
                       'iteration':False},file)
            
        # Returning a message
        if self.working_message.content=='iteration':
            return Message(object='Planning_done_iteration',
                       origin_agent='Project_manager',
                       target_agent='Software_architect')
            
        return Message(object='Planning_done',
                       origin_agent='Project_manager',
                       target_agent='Software_architect')
        
    async def wait_modification(self,document : str ='') -> Message:
        """Ask and wait for a modification into specified document"""
        
        print(Fore.GREEN + f"==> {self.__class__.__name__} is asking : Is the {document} meeting your specifications ?" + Style.RESET_ALL)
        status = True
        
        # Modification loop
        while status:
            
            instructions = f"Please modify the {document} if something is not correct.\n"
            
            if self.is_connected():
                msg = WsMessage.create_msg(object='',
                                           action='choice',
                                           agent='Project manager',
                                           msg_content=instructions + 'Are you done ?',
                                           document='Achitecture checking',
                                           model=self.llm.model_name,
                                           msg_sub_content=['Yes','No'])
                await self.websocket.send_json(data=msg)
                user_answer = (await self.websocket.receive_json())['content']['content']
                
            else:
                # Questionary event
                message = f"{self.__class__.__name__} is asking : Are you done ?"
                user_answer = await ask_user_choice_async(message=message,
                                            choices=['Yes','No'])

            # Done
            if user_answer=='Yes':
                status = False
        
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_plan_code',
                       'iteration':False},file)
            
        return Message(object='Software_design',
                       target_agent='Project_manager',
                       origin_agent='Project_manager')
    
    def plan_smaller_cycle(self,):
        return Message(object='Cycle_planned',
                       origin_agent='Project_manager',
                       target_agent='Tech_lead')
        
        