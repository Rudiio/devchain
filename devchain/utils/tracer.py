import os

import time
import numpy as np

from rich.console import Console

from dotenv import load_dotenv,find_dotenv
from langfuse.callback import CallbackHandler

from pydantic import BaseModel


def load_callback():
    """Load the langfuse callback handler"""
    load_dotenv(find_dotenv())
    
    langfuse_handler = CallbackHandler(
    public_key=os.environ['LANFUSE_PUBLIC_API'],
    secret_key=os.environ['LANFUSE_PRIVATE_API'],
    host="http://localhost:3000"
    )
    
    return langfuse_handler

console = Console()

class Tracer(BaseModel):
    nb_requests: int = 0
    starting_time : float = 0
    requests_times : list[float] = []
    mean_request_time : float = 0
    rpm : float = 0
    
    def start(self):
        """Start the tracing"""
        self.starting_time = time.time()
        
    def compute_mean_time(self,):
        """Compute the mean request duration"""
        self.mean_request_time = np.mean(self.requests_times)

    def compute_rpm(self):
        """Compute the Requests per minute metric"""
        actual_time = time.time()
        duration = (actual_time-self.starting_time)/ 60 #
        self.rpm = self.nb_requests / duration
    
    def increment_number_requests(self):
        """Increment the number of requests"""
        self.nb_requests += 1 
        
    def log_request_duration(self,duration:float):
        """Add a new request duration into the tracer"""
        self.requests_times.append(duration)
        
    def print_logs(self):
        """Print the log statistics"""
        data = self.model_dump()
        del data['requests_times']
        console.log(data)
        
        
        
        
        
        
    
    
    
    
    
    
