import time
import rich
from typing import Optional, Union
from pydantic import BaseModel, Field, InstanceOf
from colorama import Fore

from fastapi import WebSocket

from langfuse.callback import CallbackHandler

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain.prompts.base import BasePromptTemplate

from devchain.llm import load_Azure_OpenAI
from devchain.prompts.core import create_agent_prompt
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage
from devchain.rag.rag import Rag
from devchain.utils.tracer import load_callback
from devchain.utils.tracer import Tracer


class Agent(BaseModel):
    """ Representation of an agent. It is a wrapper around the Langchain agent that includes all of the specific informations 
    that are needed by DevChain.
    
    Parameters:
        role(str): Role of the agent.
        tasks(str): Main tasks of the agent.
        team_description(str): Provides team background to the agent.
        team_goal(str): Description of the goal of the team formalized based on user demand.
        agent_(Runnable): LCEL agent.
        agent(AgentExecutor): Agent executor.
        llm(Azure)
        
    """
    
    job : str = Field(description="Job of the agent in the team.")
    target_document : str = Field(description="Document that will nbe produced by the agent")
    role: str = Field(description="Role of the agent. ex: Product Owner")
    goals: str = Field(description="Description of the main goals that the agent need to do. ex : Write code, ... ")
    team_description : Optional[str] = Field(default="",description="Description of the team members.")
    team_goal : Optional[str] = Field(default="",
                                      description="Description of the goal of the team on a particular project. ex: Build a timesheet application.")
    agent : InstanceOf[Runnable] = Field(default=None,
                                          description="Langchain runnable agent that need to be executed")
    llm : Union[InstanceOf[BaseChatModel],InstanceOf[BaseLLM]]= Field(default_factory=load_Azure_OpenAI,
                                              description="LLM model that powers the agent")
    memory : list = Field(default=[],description="Buffer that stores the agent memory")
    memory_bool : bool = Field(default=False,description='True if the agents need to have memories of their actions')
    prompt :  InstanceOf[BasePromptTemplate] = Field(default=None,description="Base agent prompts that needs to be completed")
    iterations: int = Field(default=0, description="Number of iterations in the agent(number of invocation)")
    working_message : Message = Field(default=None,description="Message to work on")
    max_memory :int = Field(default=2,description="Maximum exchanges storable in the memory")
    streaming: bool = True
    working_dir : str = Field(default='',description="Folder in which the agents need to save their work")
    rag : InstanceOf[Rag] = Field(default=None,description="Rag instance to perform rag")
    callback : InstanceOf[CallbackHandler] = Field(default_factory=load_callback,description="Langfuse callback for open source tracing")
    tracer : Tracer = Field(default=None,description="Traces the statistics of the application")
    test_logic: bool = False
    websocket : Union[InstanceOf[WebSocket],None] = Field(default=None, description="Websocket that connects the backend to the front-end")
    
    def initialize_agent(self,
                         memory_bool:bool=False,
                         max_memory:int=2,
                         llm = load_Azure_OpenAI(),
                         working_dir= '',
                         rag=None,
                         callback=None,
                         tracer=None,
                         test_logic:bool=False,
                         websocket:WebSocket=None) -> None:
        
        """ Create and setup the Langchain agent inside of the class """
        # Loading the parameters
        self.memory_bool = memory_bool
        self.max_memory = max_memory
        self.llm = llm
        self.working_dir = working_dir
        self.callback = callback
        self.rag = rag
        self.tracer = tracer
        self.test_logic = test_logic
        self.websocket = websocket
        
        # Creating the prompt
        self.prompt = create_agent_prompt(self.role,self.goals,self.team_description,self.team_goal)
        
        # Chain entry arguments
        chain_args = {'mission' : lambda x : x['mission'],
                      'chat_history': lambda x : x["chat_history"],
                      'context': lambda x : x["context"]}
        
        # LCEL chain that act as the core of the agent
        self.agent = chain_args | self.prompt | self.llm| StrOutputParser()
        self.agent = self.agent.with_config({'run_name':f'{self.__class__.__name__}'})
    
    def receive_message(self,message) -> None:
        """Receive and store a new  working_message"""
        self.working_message = message
    
    def invoke(self,mission:str,context:str='')-> str:
        """Invoke the agent with a specific mission. The ouput is stored in the memory.
        
        Arguments:
            mission(str) : prompt template of the mission
        
        Return:
            The str outputed by the model"""
        
        
        args = {'mission':mission,
                'chat_history':self.memory,
                'context':context}
        
        # Running the agent executor on the specific task
        output = self.agent.invoke(args, config={"callbacks": [self.callback]})
        print(Fore.LIGHTYELLOW_EX + output)
        
        if self.memory_bool:
            # Adding the output to the memory of the agent
            self.memory.extend(
                [
                    HumanMessage(content=mission),
                    AIMessage(content=output)
                ]
            )
            if len(self.memory) > self.max_memory:
                del self.memory[0:2]
            
        self.iterations += 1
        return output
    
    async def stream(self,
                     mission:str,
                     verbose=True,
                     context:str='',
                     prefix:str=''):
        """Stream the agent with a specific mission. The ouput is stored in the memory.
        
        Arguments:
            mission(str) : prompt template of the mission
        
        Return:
            The str outputed by the model"""
        
        args = {'mission':mission,
                'chat_history':self.memory,
                'context':context}

        start = time.time()
        
        # Running the agent executor on the specific task
        output = ''
        
        # Sending the tokens to the client
        if self.is_connected():
            streaming_generator = self.agent.astream(args, config={"callbacks": [self.callback]})
            msg = WsMessage.create_msg(object=" start streaming",
                                       action="processing",
                                       document=self.target_document,
                                       model=self.llm.model_name,
                                       agent=self.job,
                                       msg_content=prefix)
            await self.websocket.send_json(msg)
            
            async for chunk in streaming_generator:
                msg = await WsMessage.acreate_msg(object="Streaming tokens",
                                       action="processing",
                                       document='TODO',
                                       model=self.llm.model_name,
                                       agent=self.job,
                                       msg_content=chunk,
                                       streaming=True)
                await self.websocket.send_json(msg)
                print(chunk,end="")
                
                output += chunk
            
        # Printing on the terminal
        else:
            streaming_generator = self.agent.stream(args, config={"callbacks": [self.callback]})
            print('\n')
            for chunk in streaming_generator:
                if verbose:
                    print(Fore.LIGHTYELLOW_EX + chunk,end="")
                output += chunk
            print('\n')
        
        if self.memory_bool:
            # Adding the output to the memory of the agent
            self.memory.extend(
                [
                    HumanMessage(content=mission),
                    AIMessage(content=output)
                ]
            )
            if len(self.memory) > self.max_memory:
                del self.memory[0:2]
        
        rich.print(f':white_check_mark: Finished [bold green]\[{time.time() - start : .3f} s][/bold green]')

        return output
    
    def is_connected(self) -> bool:
        """Check if the websocket is connected"""
        return self.websocket is not None
    
    async def execute(self,
                      mission:str,
                      verbose:bool=True,
                      context:str='',
                      log:bool=False,
                      prefix:str=''):
        """Execute a mission passed in  arguments"""
        start = time.time()
        if self.streaming:
            result = await self.stream(mission=mission,verbose=verbose,context=context, prefix=prefix)
        else: 
            result = self.invoke(mission=mission,context=context,)
        end = time.time()
        
        # Tracing
        self.tracer.log_request_duration(end-start)
        self.tracer.compute_mean_time()
        self.tracer.compute_rpm()
        self.tracer.increment_number_requests()
        
        # If you want to display the application statistics
        if log:
            self.tracer.print_logs()
            
        return result
    
    async def decide_and_act(self) -> Message:
        """Depending on the working_message decides of the action that should be executed and 
        execute it.
        In most cases, it should be overriden."""
        
        raise NotImplementedError("Specialized agent to implement")

        

        
        
        
        
    
    
    
    
