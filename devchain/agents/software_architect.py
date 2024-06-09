import json

from rich.console import Console

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.communication.document import Document
from devchain.prompts.software_architect import (write_stack,
                                                 write_file_list,
                                                 write_erd,
                                                 write_roles)
from devchain.utils.prints import print_agent_action

console = Console()

class SoftwareArchitect(Agent):
    """ Software architect agent class. Its main goal is to produce the architecture of the software:
    - global architecture
    - desing = function + classes needed + design patterns
    - system workflow + mermaid
    - choose the appropriate tech stack

    Args:
        Agent (_type_): _description_
    """
    
    job : str = "Software architect"
    target_document : str = "Software Architecture"
    role : str = "You are a software architect in a software developpment team. You are known for writting efficient, performant and adapted application designs."
    goals : str = """Your main goals consist in designing the application to facilitate its implementation and to ensure the quality of the final product."""
         
    async def decide_and_act(self) -> Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        if self.working_message is None:
            return ValueError("Communication error")

        # Need to write the product backlog if the message is the user input
        if self.working_message.object=='Planning_done' and self.working_message.origin_agent=="Project_manager":
            doc = Document.from_backlog(self.working_dir)
            return await self.write_architecture_design(title=doc.title,
                                                  user_stories=doc.user_stories,
                                                  requirements=doc.requirements,
                                                  description=doc.description)
        
        if (self.working_message.object=='Update_class_diagram_dev' or self.working_message.object=='Update_class_diagram_refine') and self.working_message.origin_agent=='Developer':
            return self.update_class_diagram()
        
        if self.working_message.object=='Planning_done_iteration' and self.working_message.origin_agent=="Project_manager":
            doc = Document.to_code(self.working_dir)
            return self.update_architecture_design_chained(title=doc.title,
                                                          user_stories=doc.user_stories,
                                                          requirements=doc.requirements,
                                                          legacy_stack=doc.stack,
                                                          legacy_design=doc.design,
                                                          legacy_file_list=doc.file_list,
                                                          legacy_common_interface=doc.dependencies)
        
    async def write_architecture_design(self,
                                  title:str,
                                  user_stories:str,
                                  requirements:str,
                                  description:str)->Message:
        """Make the software architect create the design of the application but uses prompt chaining to ensure task breakdown"""
        
        print_agent_action(agent=self,action='is designing the app')
        # Chain 1 : writting the technical stack
        with console.status(f'[bold green]{self.__class__.__name__} is choosing the tech stack [powered by {self.llm.model_name}]'):
            mission = write_stack.format(title=title,
                                        user_stories=user_stories,
                                        requirements=requirements)
            chain1 = await self.execute(mission=mission)
        
        # Chain 2 : writting the list of necessary files
        with console.status(f'[bold green]{self.__class__.__name__} is listing the files [powered by {self.llm.model_name}]'):
            mission = write_file_list.format(title=title,
                                        stack=chain1,
                                        user_stories=user_stories,
                                        requirements=requirements)
            chain2 = await self.execute(mission=mission)
        
        # Chain 3 : Writting the Files entity relationship diagram (ERD)
        with console.status(f'[bold green]{self.__class__.__name__} is designing the ERD [powered by {self.llm.model_name}]'):
            mission = write_erd.format(title=title,
                                       files=chain2,
                                       user_stories=user_stories,
                                       requirements=requirements)
            chain3 = await self.execute(mission=mission)
        
        # Chain 4 : Describe the roles and requirements of each file
        with console.status(f'[bold green]{self.__class__.__name__} is describing the roles [powered by {self.llm.model_name}]'):
            mission = write_roles.format(name=title,
                                       files=chain2,
                                       user_stories=user_stories,
                                       requirements=requirements,
                                       erd=chain3)
            chain4 = await self.execute(mission=mission)
            
        # Saving the document
        Document.save_architecture(working_dir=self.working_dir,
                                   stack=chain1,
                                   file_list=chain2,
                                   erd=chain3,
                                   roles=chain4)
        
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_code'},file)
            
        return Message(object='Software_design',
                       target_agent='Project_manager',
                       origin_agent='Software_architect',)

        
    