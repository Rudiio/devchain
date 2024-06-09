from typing import Optional, Union
from pydantic import BaseModel, Field, model_validator


class Message(BaseModel):
    """ Message for the communication between agents through the communication channel"""
    
    object: str = Field(default="",description="Object of the message,\
                it needs to be concise and clear. ex : Product backlog")
    target_agent : str = Field(default="everyone",description="Agent for whom this message is intended")
    origin_agent : str = Field(default="no one",description="Agent that emits this message")
    content : Optional[Union[dict,str]] = Field(default={},description="Content of the message ")
    
    @model_validator(mode='after')
    def check_message(self) -> 'Message':
        """Check the content of the message.
        Returns True if the message contains valid information, else otherwise"""
        
        agents = ['everyone','Product_owner','Software_architect','Developer','Tester','Senior_developer',
                  'Project_manager','Tech_lead']
        
        if len(self.object)==0:
            raise ValueError("object should not be empty")
        
        if self.target_agent not in agents:
            raise ValueError(f"Target agent should be one of {agents}")
        
        if self.origin_agent not in agents[1:] + ['User']:
            raise ValueError(f"Origin agent should be one of {agents[1:] + ['User']}")
        
        return self        
        