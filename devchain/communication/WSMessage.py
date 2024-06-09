from typing import ClassVar, Union
from pydantic import BaseModel, Field, field_validator

class WsMessage(BaseModel):
    """Model for the message that are exchanged through the websocket between the server and the client"""
    id_count : ClassVar[int]=0 # Field(default=0,description="Count of the messages id")
    id : int = Field(default=0,description="Id of the message")
    object : str = Field(default="",description="Object of the message")
    content : dict[str,Union[str,list]] = Field(default={},description="Content of the message")
    action : str = Field(default='chat', description="Action that the chat output should display")
    streaming : bool = Field(default=False,description="Indicates if the message starts a streaming sequence")
    
    @field_validator("action")
    @classmethod
    def check_action(cls,action : str):
        """Check the integrity of a Websocket message before sending it.
        The main area that field that need to be validated are action and content"""
        
        if action not in ['chat','choice','processing','OK']:
            raise ValueError("The action value should be in [chat, choice, processing]")

        return action
    
    @field_validator("content")
    @classmethod
    def check_content(cls,content : dict[str]):
        """Check the 'content' field in the model"""
        
        keys = set(content.keys())
        agents = ['everyone','Product owner','Software architect','Developer','Tester','Senior developer',
                  'Project manager','Tech lead']
        
        if keys != {'sender','model','document','content','subcontent'}:
            raise ValueError("Content keys should be {sender, model, document, content, subcontent}")
        
        if content['sender'] not in agents:
            raise ValueError(f'Sender should be in {agents}')
        
        return content
    
    @classmethod
    def create_msg(cls,
                   object:str,
                   agent : str,
                   msg_content : dict,
                   document : str,
                   model : str ='',
                   action : str = 'chat',
                   msg_sub_content : Union[list,dict,str] = '',
                   streaming: bool = False) -> dict:
        """Create a new websocket message with the correct id"""
        content = {'sender' : agent,
                   'model': model,
                   'document': document,
                   'content' : msg_content,
                   'subcontent' : msg_sub_content}
        msg = WsMessage(id = cls.id_count,
                        object=object,
                        content=content,
                        action=action,
                        streaming=streaming)
        cls.id_count += 1
        return msg.model_dump_json()
    
    @classmethod
    async def acreate_msg(cls,
                   object:str,
                   agent : str,
                   msg_content : dict,
                   document : str,
                   model : str ='',
                   action : str = 'chat',
                   msg_sub_content : Union[list,dict,str] = '',
                   streaming: bool = False) -> dict:
        """Create a new websocket message with the correct id"""
        content = {'sender' : agent,
                   'model': model,
                   'document': document,
                   'content' : msg_content,
                   'subcontent' : msg_sub_content}
        msg = WsMessage(id = cls.id_count,
                        object=object,
                        content=content,
                        action=action,
                        streaming=streaming)
        cls.id_count += 1
        return msg.model_dump_json()