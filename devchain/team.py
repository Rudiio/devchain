import time
import yaml
from typing import Union
import os
import shutil
import rich

from colorama import Fore, Style
from pydantic import BaseModel, Field, InstanceOf
from fastapi import WebSocket

from devchain.communication.communication_channel import CommunicationChannel
from devchain.communication.WSMessage import WsMessage
from devchain.agents.agent import Agent
from devchain.agents.product_owner import ProductOwner
from devchain.agents.project_manager import ProjectManager
from devchain.agents.software_architect import SoftwareArchitect
from devchain.agents.tech_lead import TechLead
from devchain.agents.developer import Developer
from devchain.agents.senior_developer import SeniorDeveloper
from devchain.agents.tester import Tester
from devchain.communication.message import Message
from devchain.communication.document import Document
from devchain.utils.io import create_folder,clean_folder,ask_user_choice
from devchain.utils.tracer import load_callback, Tracer
from devchain.llm import load_llm
from devchain.rag.rag import Rag
from devchain.rag.code_context_retriever import CodeContextRetriever

from langfuse.callback import CallbackHandler

        
class Team(BaseModel):
    """Software developpment team. It is the main agents orchestration tool.
    
    Parameters:
    """
    members: dict[str,Agent] = Field(default={},description="Team members")
    channel: InstanceOf[CommunicationChannel] = Field(default=CommunicationChannel(),description="Communication interface for the\
                                                        team members")
    message_notification : bool = Field(default=False,description="Notifies if there is a new message")
    developping : bool = Field(default=False,description="Bool managing the developpment loop")
    max_developpment_iterations : int = Field(default=2, description= "The maximum number of time the deliverable can loop between developer and devexecutor")
    max_testing_iterations : int = Field(default=2,description="The maximum number of time the deliverable can be tested")
    working_dir : str = Field(default='', description="Name of the generated folder")
    rag : InstanceOf[Rag] = Field(default=None,description="Rag instance to perform rag")
    callback : InstanceOf[CallbackHandler] = Field(default=None,description='Langfuse Callback handler')
    tracer : Tracer = Field(default=None,description="Traces the statistics of the application")
    test_logic : bool = False
    websocket : Union[InstanceOf[WebSocket],None] =  Field(default=None,description="Websocket that connects the backend to the front-end")
    
    def initialize(self) -> None:
        """Initialize the team and the team members.
        Deprecated, use the from_config method instead."""
        
        # Create the folder
        self.setup_environnment()
        
        self.state = "Hiring team members"
        self.monitoring()
        
        self.members = {'Product_owner' : ProductOwner(streaming=True),
                        'Software_architect': SoftwareArchitect(streaming=True),
                        'Developer' : Developer(streaming=True),
                        'Senior_developer': SeniorDeveloper(streaming=True),
                        'Tester': Tester(streaming=True)}
        
        self.state = 'Briefing everyone'
        self.monitoring()
        
        # Initializating the team
        for agent in self.members.keys():
            self.members[agent].initialize_agent(streaming=True,
                                                 )
        
    async def start(self,request:str='',message:Message=None) -> None:
        """Start the developpment process by sending the user demand into the channel.
        
        Arguments:
            request(str): software/application demand submitted by the user.
        """
        # The project is restarting : save the request and create a new folder
        if request != '':
            self.setup_python_environnment(self.working_dir)
            # Save the User request
            Document.save_informations(working_dir=self.working_dir,info={'Request':request})
            self.monitoring("Your demand has been transmitted to the Product Owner")

            if self.is_connected():
                msg = WsMessage.create_msg(object="Starting the project the project",
                                        agent='Project manager',
                                        document='Request',
                                        msg_content="Your demand has been transmitted to the Product Owner.",
                                        action='processing')
                await self.websocket.send_json(data=msg)
            
        else:
            self.monitoring("Resuming the project from the selected state.")
            
            if self.is_connected():
                msg = WsMessage.create_msg(object="Resuming the project",
                                        agent='Project manager',
                                        document='Resuming',
                                        msg_content="Resuming the project from the selected state.",
                                        action='processing')
                await self.websocket.send_json(data=msg)
            
        self.message_notification = self.channel.receive_message(message=message)
    
    async def run_sprint(self) -> bool:
        """Run the developpment process"""
        self.developping = True
        
        loop_count = 0
        self.tracer.start()
        while self.developping:
            # Retrieving the message from the channel
            current_message = self.channel.retrieve_message()
            
            # Agentic logic
            acting_agent = current_message.target_agent
            acting_agent = self.members[acting_agent]
            acting_agent.receive_message(current_message)
            
            # Display state
            # self.monitoring()
            new_message = await acting_agent.decide_and_act()
            
            # Logic to cap the testing loop
            if new_message.origin_agent=='Senior_developer': 
                loop_count += 1
            if loop_count % self.max_testing_iterations==0 and new_message.origin_agent=='Senior_developer' and new_message.object=="Code_to_debug":
                state_message = await self.handle_stop()
                if state_message is not None:
                    new_message = state_message
                    
                loop_count +=1
                 
            # Storing the new message
            self.message_notification = self.channel.receive_message(new_message)
            
            # Ending the {working_dir}
            if new_message.object=="END":
                # Moving the current sprint into done
                if new_message.content == 'move to done':
                    source = f'{self.working_dir}/current_sprint/'
                    destination = f'{self.working_dir}/done/'
                    files = os.listdir(source)
                    files.sort()
                    for file in files:
                        src = source + file
                        dst = destination + file
                        shutil.move(src,dst)
                        
                self.developping = False
                
            # To avoid the time-token limit imposed by Azure OpenAI
            # TODO : replace with RPM controller
            time.sleep(1)

    async def handle_stop(self):
        """Handle the stopping events when the maximum number of iterations is reached"""
        choices = ['Make another development loop','Stop the development process']
        
        if self.is_connected():
            msg = WsMessage.create_msg(object="Stop event",
                                        agent='Project manager',
                                        document='Project State',
                                        msg_content="You reached the setted maximum number of development iterations. Do you want to make another iteration or to stop the process ?",
                                        action='choice',
                                        msg_sub_content=choices)
            await self.websocket.send_json(data=msg)
            response = (await self.websocket.receive_json())['content']['content']
        else:
            print(Fore.RED + "==> Max number of Development iterations reached" + Style.RESET_ALL)
            response = ask_user_choice(message='What do you want to do ?',
                                        choices=choices)
        
        # Stopping the development process
        if response=='Stop the development process':
            print(Fore.RED + "==> Stopping development, triggering the Product owner" + Style.RESET_ALL)
            return Message(object='Project_aborted',
                                target_agent='Product_owner',
                                origin_agent='Senior_developer',)
        else:
            return None
                    
    @classmethod
    def monitoring(cls, string:str)->None:
        """ Allows to monitor the state of the app.
        First : basic prints.
        Second : more visual.
        Third : api call to the frontend"""
    
        rich.print(f':loudspeaker: {string}')
    
    @classmethod
    def setup_python_environnment(self,working_dir:str) -> None:
        """Create the folder in which the team will lead the {working_dir} and put the deliverables"""
        
        # Creating the folder
        create_folder(f"./{working_dir}")
        clean_folder(f'./{working_dir}')
        
        # Creating the __init__.py
        # create_file(f"./{working_dir}/__init__.py",overwrite=True)
            
        # creating the backlog folder 
        create_folder(f"./{working_dir}/backlog")
        clean_folder(f"./{working_dir}/backlog")
        
        # creating the requirements folder
        create_folder(f"./{working_dir}/requirements")
        clean_folder(f"./{working_dir}/requirements")

        # creating the current sprint folder
        create_folder(f'./{working_dir}/current_sprint')
        clean_folder(f'./{working_dir}/current_sprint')
        
        # creating the done folder
        create_folder(f'./{working_dir}/done')
        clean_folder(f'./{working_dir}/done')
        
        # creating the review folder
        create_folder(f'./{working_dir}/reviews')
        clean_folder(f'./{working_dir}/reviews')
        
        # creating the src folder
        create_folder(f"./{working_dir}/src")
        clean_folder(f"./{working_dir}/src")
        
        # creating misc folder
        create_folder(f"./{working_dir}/misc")
        clean_folder(f"./{working_dir}/misc")
        
        # Initializating __init__.py
        file = open(f'./{working_dir}/src/__init__.py','+a')
        file.write("import os\n")
        file.write("import sys\n")
        file.write("path = os.getcwd()\n")
        file.write("SOURCE_PATH = os.path.join(path,'src')\n")
        file.write("sys.path.append(SOURCE_PATH)")
        file.close()
        
        # Creating the tests folder
        create_folder(f"./{working_dir}/tests")
        clean_folder(f"./{working_dir}/tests")

        # Creating a __init__.py for the tests
        file = open(f'./{working_dir}/tests/__init__.py','+a')
        file.write("import os\n")
        file.write("import sys\n")
        file.write("path = os.getcwd()\n")
        file.write(f"SOURCE_PATH = os.path.join(path,'{working_dir}/src')\n")
        file.write("sys.path.append(SOURCE_PATH)")
        file.close()
    
    def is_connected(self) -> bool:
        """Check if the websocket is connected"""
        return self.websocket is not None
    
    @classmethod
    def from_config(cls,config:str='./config/config.yaml',working_dir:str='generated_project',test_logic:bool=False,websocket:WebSocket=None):
        """Create a team directly from a config.yaml file"""
        
        # Loading the file
        print(f"Reading {config} file")
        with open(config,'r+') as file:
            parameters = yaml.safe_load(file)
            
            # Creating the team
            team = Team(max_developpment_iterations=parameters['Team']['max_developpment_iterations'],
                        max_testing_iterations=parameters['Team']['max_testing_iterations'],
                        working_dir=working_dir,
                        test_logic=test_logic,
                        websocket=websocket)
        
            # Langfuse callback
            team.callback = load_callback()
            
            # Creating the members
            cls.monitoring("Hiring team members")

            team.members = {'Product_owner' : ProductOwner(),
                        'Project_manager' : ProjectManager(),
                        'Software_architect': SoftwareArchitect(),
                        'Tech_lead' : TechLead(),
                        'Developer' : Developer(),
                        'Senior_developer': SeniorDeveloper(),
                        'Tester': Tester()}
            
            cls.monitoring('Briefing everyone')
            
            members_config = parameters['Team']['members']
            
            # rag
            # team.rag = CodeRag(callback=team.callback,persist_directory=f'{team.working_dir}/vectordb')
            team.rag = CodeContextRetriever(working_dir=team.working_dir)
            team.rag.setup_rag()
            
            # Tracer
            team.tracer = Tracer()
            
            # Initializating the team
            for agent in team.members.keys():
                team.members[agent].initialize_agent(memory_bool=members_config[agent]['memory']['memory_bool'],
                                                     max_memory=members_config[agent]['memory']['max_memory'],
                                                     llm = load_llm(kind=members_config[agent]['llm']['kind'],
                                                                    model=members_config[agent]['llm']['model'],
                                                                    temperature=members_config[agent]['llm']['temperature']),
                                                     working_dir=team.working_dir,
                                                     rag=team.rag,
                                                     callback=team.callback,
                                                     tracer=team.tracer,
                                                     test_logic=test_logic,
                                                     websocket=websocket)
            return team
            
            
            

            
                
        
        
        
        
        
