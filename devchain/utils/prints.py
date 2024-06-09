from rich.console import Console
from rich.panel import Panel
from rich import print
from devchain.agents.agent import Agent


console = Console()


def print_agent_action(agent:Agent,action:str):
    """Print the action that the agent will perform"""
    
    console.print(f":robot: [bold green]{agent.__class__.__name__}[/bold green] [green]{action} \[powered by {agent.llm.model_name}] [/green]")
    

def print_headers():
    """Prints the header of the application"""
    banner = """
    =============================== < 🦙 /> [bold]DevChain[/bold] ==========================
    🚀 Build software by using a meta-programming and multi-agent AI system. 🚀"
    Mantu                                                                v0.2.1 
    ===========================================================================
    This first version implements the main features but is still in 
    developpment and the output can be unstable\n"""
    print(Panel.fit(banner))
    