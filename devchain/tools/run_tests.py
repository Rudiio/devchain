
import subprocess
from typing import Type

from colorama import Fore, Style

from pydantic import BaseModel, Field

from devchain.utils.io import handle_requirements

class RunCodeInput(BaseModel):
    tests : str = Field(description="The tests that need to be runned")
    programming_language : str = Field(description="The programming language of the tests")

class RunTests(BaseModel):
    name : str = "run_tests"
    description : str = "useful when you need to run some tests"
    args_schema : Type[BaseModel] = RunCodeInput
    
    def __call__(self,
                 working_dir:str='',
                 requirements:str='') -> str:
        
        # Identify the programming language
        command = self._identify_command()
        
        # Verify the arguments types
        print(Fore.RED + "==> Handling requirements " + Style.RESET_ALL)
        
        # Install the requirements
        handle_requirements(requirements=requirements)
        
        # Identify the command to execute
        print(Fore.RED + f"==> Running the command : {' '.join(command)} " + Style.RESET_ALL)
        timeout = 20
        cwd = working_dir
        
        # Launching the process
        process = subprocess.Popen(command,
                                   cwd=cwd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   )
        # Putting a timeout
        try:
            stdout,stderr = process.communicate(timeout=timeout)
        
        # Handling the timeout
        except subprocess.TimeoutExpired:
            process.kill()
            stdout,stderr = process.communicate()
    
        return stdout.decode('utf-8'),stderr.decode('utf-8')
    
    def _identify_command(self) -> tuple[list[str],str]:
        return ['pytest','tests','--tb=short']
    
         
                
            
    
    
    