import json

from rich.console import Console

from devchain.agents.agent import Agent
from devchain.communication.message import Message
from devchain.communication.document import Document
from devchain.prompts.developer import write_code_task,refine_code_task, select_code_context
from devchain.utils.io import pop_save_json
from devchain.utils.prints import print_agent_action

console = Console()

class Developer(Agent):
    """Developer agent class. Its main goal is to write the code of the application. It works like a real developer and writes the code step-by-step
    by following a coding plan that is composed of several tasks.
    """
    job : str = "Developer"
    target_document : str = "Code"
    role : str = """You are a professional software developer in a software developpement team. You write elegant, reliable and reusable code."""
    goals: str = """You write code by following specific instructions and follow the architecture and design of the project by the letter to ensure qualitative product."""
    memory_bool : bool = False
    
    async def decide_and_act(self,)->Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it"""
        
        # Devchain code writting loop 
        if (self.working_message.object=='Code_plan' and self.working_message.origin_agent=='Tech_lead') or (self.working_message.object=='Resume_coding' and self.working_message.origin_agent=='Software_architect'):
            # Load the plan as a list
            plan = Document.load_plan(path=f'{self.working_dir}/misc/plan.json')
            return await self.code_writting_session(plan=plan)
        
        # Devchain code correction loop
        if self.working_message.object=='Code_to_debug' and (self.working_message.origin_agent=='Senior_developer' or self.working_message.origin_agent=='Software_architect'):
            fixes = Document.load_fixes(path=f'{self.working_dir}/misc/fixes.json')
            return await self.code_refining_session(fixes=fixes)
    
    async def code_writting_session(self,plan:list[dict]):
        """Launch the code writting based on the plan"""
        
        if len(plan)>0:
            print_agent_action(agent=self,action='is writting the code')
            
        shared_doc = Document.to_code(self.working_dir)

        # Solving the tasks one by one
        for n in range(len(plan)):
            task = plan[n]
            self.target_document = f"Code : `{task['file']}`"
            
            # Retrieve the code to modify
            legacy_code = Document.load_file(f"{self.working_dir}/src/{task['file']}")

            # Format the prompt
            mission = write_code_task.format(name=shared_doc.title,
                                             description=shared_doc.description,
                                             file = task['file'],
                                             code=legacy_code,
                                             erd=shared_doc.erd,
                                             files=shared_doc.roles,
                                             stack=shared_doc.stack,
                                             task_description=task['description'],
                                             task_technology=task['technology'],
                                             task_instructions=task['instructions'])
            
            # Retrieve the code context based on the dependencies
            selected_context = await self.select_code_context(name=shared_doc.title,task=task,erd=shared_doc.erd,roles=shared_doc.roles)
            code_context=''
            if self.rag.retriever is not None:
                if len(select_code_context)>0:
                        code_context = self.rag.invoke(selected_context,file_path=f"{self.working_dir}/src/{task['file']}")
            
            # Execute the task
            console.log(task)
            with console.status(f"[bold green]{self.__class__.__name__} is solving task #{task['id']} (total={plan[-1]['id']})"):
                code = await self.execute(mission=mission,context=code_context)

            # Saving the code file in the right folder
            path = Document.save_code(code=code,path=f"{self.working_dir}/src/{task['file']}")
            
            # Loading the produced code
            self.rag.load_documents(document_path=path)
            
            # Pop the task
            pop_save_json(field='tasks',iter=plan[n+1:],path=f'{self.working_dir}/misc/plan.json')

        
        if self.test_logic:
            # Saving the state of the project
            with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_design_tests'},file)
            
            return Message(object='Code_to_test',
                            target_agent='Tester',
                            origin_agent='Developer')
        else:
            # Saving the state of the project
            with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_review'},file)
                
            return Message(object='Review',
                        target_agent='Senior_developer',
                        origin_agent='Tester',)
    
    async def code_refining_session(self,fixes:list[dict])->Message:
        """Launch a code refining session based on the fixes that need to be applied"""
        
        print_agent_action(agent=self,action='is refining the code')
        shared_doc = Document.to_code(self.working_dir)
    
        for n in range(len(fixes)):
            fix = fixes[n]
            self.target_document = f"Code refining : `{fix['file']}`"
            
            # Retrieve the code to modify
            legacy_code = Document.load_file(f"{self.working_dir}/src/{fix['file']}")
            
            
            # Format the prompt
            mission = refine_code_task.format(name=shared_doc.title,
                                             file = fix['file'],
                                             code=legacy_code,
                                             files=shared_doc.roles,
                                             fix_description=fix['description'],
                                             fix_technology=fix['technology'],
                                             fix_issue=fix['issue'],
                                             fix_instructions=fix['instructions'],
                                             erd=shared_doc.erd)

            # Retrieve the code context based on the dependencies
            selected_context = await self.select_code_context(name=shared_doc.title,task=fix,erd=shared_doc.erd,roles=shared_doc.roles)
            code_context=''
            if self.rag.retriever is not None:
                if len(select_code_context)>0:
                        code_context = self.rag.invoke(selected_context,file_path=f"{self.working_dir}/src/{fix['file']}")
    
            # Execute the tasks
            console.log(fix)
            with console.status(f"[bold green]{self.__class__.__name__} is applying fix #{fix['id']} (total={fixes[-1]['id']})"):
                new_code = await self.execute(mission=mission,context=code_context)
            
            # Saving the code file in the right folder
            path = Document.save_code(path=f'{self.working_dir}/src/{fix["file"]}',code=new_code)
            
            # Loading the produced code
            self.rag.load_documents(document_path=path)
            
            # Pop the task
            if n==len(fixes)-1:
                iter = []
            else:
                iter = fixes[n+1:]
            pop_save_json(field='fixes',iter=iter,path=f'{self.working_dir}/misc/fixes.json')
            

        if self.test_logic:
            # Saving the state of the project
            with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_debug_tests'},file)
                
            return Message(object='Tests_to_debug',
                        target_agent='Tester',
                        origin_agent='Developer',)
        else:
            # Saving the state of the project
            with open(f'{self.working_dir}/misc/log.json','w+') as file:
                json.dump({'state':'to_review'},file)
                
            return Message(object='Review',
                        target_agent='Senior_developer',
                        origin_agent='Tester',)
    
    async def select_code_context(self,
                            name:str,
                            task:dict,
                            erd:str,
                            roles:str):
        """Select the code context needed"""
        print_agent_action(agent=self,action='is selecting the context')
        mission = select_code_context.format(name=name,
                                             task_file=task['file'],
                                             task_description=task['description'],
                                             task_technology=task['technology'],
                                             task_instructions=task['instructions'],
                                             erd=erd,
                                             files=roles,
                                             codebase = self.rag.dump())
        
        with console.status(f"[bold green]{self.__class__.__name__} is selecting the right context"):
            context = Document.parser.parse_code(await self.execute(mission=mission,context='',
                                                                    prefix=f"I will need the following code context to write `{task['file']}`:\n"))
        
        return Document.parser.parse_python_list(context)
        