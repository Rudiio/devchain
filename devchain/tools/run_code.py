import os
import asyncio
import signal
import subprocess
from typing import Type

from colorama import Fore, Style

from pydantic import BaseModel, Field
from fastapi import WebSocket

from devchain.communication.WSMessage import WsMessage
from devchain.utils.io import handle_requirements

class RunCodeInput(BaseModel):
    code : str = Field(description="The code that need to be executed")
    programming_language : str = Field(description="The programming language of the code")

class RunCode(BaseModel):
    name : str = "run_code"
    description : str  = "useful when you need to run some code but not appropriate for testing"
    args_schema : Type[BaseModel] = RunCodeInput

    async def __call__(self,
                 requirements:str,
                 working_dir:str,
                 websocket:WebSocket=None) -> str:
        
        # Identify the programming language
        command = self._identify_command(working_dir=working_dir)
        
        # Verify the arguments types
        print(Fore.RED + "==> Handling requirements " + Style.RESET_ALL)
        
        # Install the requirements
        handle_requirements(requirements=requirements)
        
        # Identify the command to execute
        timeout = 15
        if websocket is not None:
            msg = WsMessage.create_msg(object='',
                                        action='processing',
                                        agent="Senior developer",
                                        msg_content= f"Running the command : `{' '.join(command)}`  [timeout={timeout}s]",
                                        document='Code execution',
                                        model="None")
            await websocket.send_json(data=msg)
        else:
            print(Fore.RED + f"==> Running the command : {' '.join(command)}  [timeout={timeout}s]" + Style.RESET_ALL)
        await asyncio.sleep(1)
        
        # Launching the process
        process = subprocess.Popen(command,
                                   cwd=f'{working_dir}/src/',
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # Putting a timeout
        try:
            stdout,stderr = process.communicate(timeout=timeout)
        # Handling the timeout
        except subprocess.TimeoutExpired:
            # Send a CTRL-C signal to end the application
            os.kill(process.pid,signal.SIGINT)
            stdout,stderr = process.communicate()
        return stdout.decode('utf-8'),stderr.decode('utf-8')
    
    def _identify_command(self,working_dir:str) -> tuple[list[str],str]:
        for file in os.listdir(f'./{working_dir}/src'):
            if os.path.isfile(f'./{working_dir}/src/{file}'):
                name,ext= file.split(sep='.')
                if name == 'main' or name =='app' or name=='application':
                    if ext =='py':
                        return ['python3',file]
            
        return None
    
    def _handle_requirements(self,requirements:list,programming_language:str):
        # Installing the packages if needed
        handle_requirements(programming_language=programming_language,
                            requirements=requirements)
         
                
            
    
    
    