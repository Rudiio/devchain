from pydantic import BaseModel,Field
from devchain.communication.message import Message

class CommunicationChannel(BaseModel):
    """Communication channel/pool for the agent. They can send and retrieve messages from this channel 
    It contains a message queue and a dict that stores the deliverables
    
    Parameters:
        """
        
    messages: list[Message] = Field(default=[],description="List of messages emmitted in the pool\
        The most important is the last one as it is the one that define the next action to execute.")
    
    def receive_message(self,message : Message) ->  bool:
        """Receives and stores a message in the communication channel
        
        Arguments:
            message(Message) : message to store in the channel"""
        
        self.messages.append(message)
        
        return True
    
    def retrieve_message(self) -> Message:
        """Send the last message to the an agent"""
        
        if len(self.messages)==0:
            return ValueError("No messages stored into the channel")
        
        return self.messages[-1]

        
