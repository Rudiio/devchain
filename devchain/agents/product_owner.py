import json
from colorama import Fore

from rich.console import Console

from devchain.agents.agent import Agent
from devchain.prompts.product_owner import write_backlog, write_new_features
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage
from devchain.communication.document import Document
from devchain.utils.io import ask_user_choice_async,ask_user_question
from devchain.utils.prints import print_agent_action
console = Console()

class ProductOwner(Agent):
    """ 
    Product owner agent class. Its main goal is to write the backlog : user stories and requirements for the system.
    The User stories are composed of 2 main components:
        - the user stories ex : As a [user] 
        I want a [functionality] so that [benefit]
        - the acceptance criteria 
        ex: Given [how things begin]
        When [action taken]
        Then [outcome of taking action]
    
    The requirements consist of :
        - an introduction
        - an overall descrition
        - Functionnal requirements
        - Non-functionnal requirements
    
    """
    job : str = "Product owner"
    target_document : str = "Product backlog"
    role : str = "You are a Product Owner in a software developpement team. You understand the request and needs of the client and write a meaningful backlog."
    goals: str = "Your main goals consist in understand the needs of the stakeholders and write a corresponding, precise and realist backlogs for applications."
    streaming : bool = True
        
    async def decide_and_act(self) -> Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        if self.working_message is None:
            return ValueError("Communication error")

        # Need to write the product backlog if the message is the user input
        if self.working_message.object=='User_request' and self.working_message.origin_agent=="User":
            document = Document.load_informations(self.working_dir)
            return await self.write_backlog(request=document.user_request)

        # The project succeed
        if self.working_message.object=='Project_completed' and self.working_message.origin_agent=="Senior_developer":
            if self.is_connected():
                msg = WsMessage.create_msg(object='',
                                           action='OK',
                                           agent=self.job,
                                           msg_content="The development ended successfully✅.\nThe user_stories and the requirements are will be putted into the `done` folder.",
                                           document='Review',
                                           model=self.llm.model_name)
                await self.websocket.send_json(data=msg)
            else:
                print("==> The development ended successfully <==")
                print("The user_stories and the requirements are will be putted into the `done` folder")
            return Message(object="END",
                           target_agent="everyone",
                           origin_agent="Product_owner",
                           content='move to done')
        
        # Start a new iteration
        if self.working_message.object=='Add_new_features' and self.working_message.origin_agent=='User':
            document = Document.from_done_backlog(self.working_dir)
            return self.write_new_features(name=document.title,
                                           legacy_user_stories=document.user_stories,
                                           legacy_requirements=document.requirements)
        
        # The project failed
        if self.working_message.object=='Project_aborted' and self.working_message.origin_agent=="Senior_developer":
            if self.is_connected():
                msg = WsMessage.create_msg(object='',
                                           action='choice',
                                           agent=self.job,
                                           msg_content="The development was ended❌.\nDo you want to put the current sprint's user stories and requirements into the `done` folder ?",
                                           msg_sub_content=['Yes','No'],
                                           document='Review',
                                           model=self.llm.model_name)
                await self.websocket.send_json(data=msg)
                response = (await self.websocket.receive_json())['content']['content']
            else:  
                print("==> The project was ended <==")
                response = await ask_user_choice_async(message="Do you want to put the current sprint's user stories and requirements into the `done` folder ?",
                                        choices=['Yes','No'])
                
            if response == 'Yes':
                return Message(object="END",
                            target_agent="everyone",
                            origin_agent="Product_owner",
                            content='move to done')
            else:
                return Message(object="END",
                            target_agent="everyone",
                            origin_agent="Product_owner",
                            )

    async def write_backlog(self,request) -> Message:
        """ Write the backlog of the project"""
    
        print_agent_action(agent=self,action='is cooking the backlog')
        with console.status(f'[bold green]{self.__class__.__name__} is cooking the backlog [powered by {self.llm.model_name}]'):
            # Make the agent write the backlog
            mission = write_backlog.format(request=request)
            backlog = await self.execute(mission=mission)
    
        # saving the deliverable as markdown
        Document.save_backlog(backlog=backlog,working_dir=self.working_dir)
        
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_plan_sprint'},file)
            
        # Return the message
        return Message(
            object="Product_backlog_to_plan",
            target_agent="Project_manager",
            origin_agent="Product_owner",
        )
    
    def write_new_features(self,
                           name:str,
                           legacy_user_stories:str,
                           legacy_requirements:str)->Message:
        """Make the Product owner write a new backlog related to the asked new feature."""
        
        request = ask_user_question(question='What features do you want to add ?')
        
        mission = write_new_features.format(name=name,
                                            new_features=request,
                                            legacy_user_stories=legacy_user_stories,
                                            legacy_requirements=legacy_requirements)
        
        print(Fore.GREEN + f'==> {self.__class__.__name__} is cooking the backlog [powered by {self.llm.model_name}]')
        
        # PO writes the backog
        with console.status(f'[bold green]{self.__class__.__name__} is cooking the backlog [powered by {self.llm.model_name}]'):
            new_backlog = self.execute(mission=mission)
        
        # saving the deliverable as markdown
        Document.save_backlog(backlog=new_backlog,working_dir=self.working_dir)
        
        # Saving the state of the project
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'update_design',
                       'iteration':True},file)
            
        # Return the message
        return Message(
            object="Product_backlog_to_plan",
            target_agent="Project_manager",
            origin_agent="Product_owner",
            content='iteration'
        )
    
