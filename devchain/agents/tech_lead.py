import json
from rich.console import Console

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.communication.document import Document
from devchain.prompts.tech_lead import plan_code, translate_plan_code
from devchain.utils.prints import print_agent_action

console = Console()

class TechLead(Agent):
    """ 
    tech lead agent class. Its main goal is to plan the coding session that will be ran to implement the application based on the backlog and architecture.
    """
    job :str = "Tech lead"
    target_document : str = "Plan"
    role : str = "You are the Technical lead of your company, as a former developper, you have a strong technical background in computer science. You acquired strong capabilities in code planning."
    goals: str = "Create precise step-by-step plan to implement applications."
    streaming : bool = True
        
    async def decide_and_act(self) -> Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        if self.working_message is None:
            return ValueError("Communication error")
        
        if self.working_message.object=='Cycle_planned' and self.working_message.origin_agent=='Project_manager':
            doc = Document.to_code(self.working_dir)
            return await self.plan_code_writting(name=doc.title,
                                           erd=doc.erd,
                                           stack=doc.stack,
                                           file_description=doc.file_description,
                                           description=doc.description,
                                           roles=doc.roles)
            
        if self.working_message.object=='Testing_to_plan' and self.working_message.origin_agent=='Tester':
            doc = Document.to_code_tests(working_dir=self.working_dir)
            return self.plan_tests_writting(name=doc.title,
                                            testcases=doc.testcases,
                                            test_stack=doc.testing_stack,
                                            code_files_description=doc.file_description,
                                            test_files_description=doc.test_files_description,
                                            front=doc.front)
            
    async def plan_code_writting(self,
                           name:str,
                           stack:str,
                           erd:str,
                           file_description:list[str],
                           description:str,
                           roles:str)->Message:
        """Write the code plan that will be used by the Developer to write the application."""
        
        print_agent_action(self,action='is planning the code writting')
        
        with console.status(f'[bold green]{self.__class__.__name__} is describing the plan [powered by {self.llm.model_name}]'):
            mission = plan_code.format(name=name,
                                       description=description,
                                       stack=stack,
                                       erd=erd,
                                       files=roles,)
            plan = await self.execute(mission=mission,verbose=True)
        
        with console.status(f'[bold green]{self.__class__.__name__} is translating the plan [powered by {self.llm.model_name}]'):
            mission = translate_plan_code.format(name=name,
                                       plan=plan,
                                       files=roles,
                                       stack=stack,
                                       erd=erd)
            plan = await self.execute(mission=mission,verbose=True)
        
        # Parse the plan and save it
        plan = Document.parser.parse_code(plan)
        with open(f'{self.working_dir}/misc/plan.json','w+') as file:
            file.write(plan)
        
        # Saving the state
        with open(f'{self.working_dir}/misc/log.json','w+') as file:
            json.dump({'state':'to_code',
                       'iteration':False},file)
            
        return Message(object='Code_plan',
                       target_agent='Developer',
                       origin_agent='Tech_lead')
        
    # def plan_tests_writting(self,
    #                         name:str,
    #                         testcases:str,
    #                         test_stack:str,
    #                         class_diagram:str,
    #                         code_files_description:str,
    #                         test_files_description:str,
    #                         front:str)->Message:
    #     """Write the plan to write the tests that will be used by the tester to write the tests"""
        
    #     print(self,'is planning the tests writting')
    #     with console.status(f'[bold green]{self.__class__.__name__} is writting the tasks [powered by {self.llm.model_name}]'):
    #         mission = plan_tests_writting.format(name=name,
    #                                              stack=test_stack,
    #                                              testcases=testcases,
    #                                              class_diagram=class_diagram,
    #                                              files_description=code_files_description,
    #                                              test_files=test_files_description,
    #                                              front=front)
            
    #         test_plan = self.execute(mission=mission,verbose=True)
            
    #     # Parse the plan and save it
    #     test_plan = Document.parser.parse_code(test_plan)
    #     with open(f'{self.working_dir}/misc/test_plan.json','w+') as file:
    #         file.write(test_plan)
        
    #     # Saving the state
    #     with open(f'{self.working_dir}/misc/log.json','w+') as file:
    #         json.dump({'state':'to_code_tests',
    #                    'iteration':False},file)
            
    #     return Message(object='Tests_to_write',
    #                    target_agent='Tester',
    #                    origin_agent='Tech_lead')
        
        
        
        
        
        
        
        