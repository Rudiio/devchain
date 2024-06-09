""" The prompts for the project are strored here.
These prompts are actually strings in which the it is needed to inject some informations"""

from langchain_core.prompts import (ChatPromptTemplate,
                                    MessagesPlaceholder,
                                    PromptTemplate,
                                    SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate)


def create_agent_prompt(role:str,goals:str,team_description:str,
                        team_goal:str,):
    """Create the prompt for the base prompt for the base agent"""
    
    # Template creation
    # Can be customized as needed
    template = "**Role**: {role}\n**Goals**:{goals}\n"
                
    if team_description!="":
        template += "**team_description**: {team_description}\n"
    
    if team_goal!="":
        template += "**team_description**: {team_goal}\n\n"
    
    # Using Chatprompttemplate + message interface is better than simple template prompting
    # It allows langchain to automatically separates the messages and feedback from tools
    prompt = ChatPromptTemplate.from_messages(
    [
       SystemMessagePromptTemplate.from_template(template=template),
       MessagesPlaceholder(variable_name='chat_history',optional=True),
       HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['mission'],template='{mission}')),
       HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['context'],template='\n{context}'))
    ]
)
    return prompt.partial(role=role,goals=goals,team_description=team_description,team_goal=team_goal)




