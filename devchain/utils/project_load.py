import os
import asyncio
import json

from fastapi import WebSocket

from collections import defaultdict

from devchain.communication.document import Document
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage

async def identify_existing_project(working_dir:str='generated_project',
                              test_logic:bool=False,
                              websocket:WebSocket=None) -> Message:
    """Serves to identify if the a project already exist in the folder"""
    
    # Checking if the folder already exists
    folder_exist = os.path.exists(working_dir)
    
    # Check the existing documents 
    if folder_exist:
        # Processing to check if the files that are present
        present_documents = identify_present_files(working_dir=working_dir)
        state_informations = log_project_state(working_dir=working_dir,
                                               present_doc=present_documents)
        
        choices = ['Resume the development from last state',
                    'Choose a starting state',
                    'Overwrite the folder']
        
        # Checking if new features can be added
        if present_documents['done'] > 0 and present_documents['current_sprint']==0:
            state = 'update_app'
            choices = ['Add new features',
                       'Overwrite the folder']
            
        # Exctract the project state from the misc/log.json
        elif not os.path.exists(f'{working_dir}/misc/log.json'):
            state = 'to_start'
            iteration=False
            
        else:
            with open(f'{working_dir}/misc/log.json','r+') as file:
                log = json.load(file)
                state = log['state']
                iteration = False
                if 'iteration' in log:
                    iteration = log['iteration']
        
        state_informations += f"☄️ The state of the project is `{state}`.\n"
        
        msg = WsMessage.create_msg(object="Project state",
                                   agent="Project manager",
                                   action='processing',
                                   msg_content=state_informations,
                                   document="workspace",
                                   model='')
        await websocket.send_json(msg)
        
        await asyncio.sleep(2)
        
        # Sending the annoucement message
        msg = WsMessage.create_msg(object="choice demand",
                                   agent="Project manager",
                                   action='choice',
                                   msg_content="Do you want to overwrite the folder or resume the previous process ?",
                                   msg_sub_content=choices,
                                   document="workspace",
                                   model='')
        await websocket.send_json(msg)
        response = (await websocket.receive_json())['content']['content']
        
        # Need to overwrite the folder
        if response=='Overwrite the folder':
            return None
        
        # Lazy resuming from last state
        elif response=='Resume the development from last state':
            return get_starting_message(state=state)
        
        # Add new features into the app
        elif response == 'Add new features':
            return Message(object='Add_new_features',
                           target_agent='Product_owner',
                           origin_agent='User')
            
        # Choosing a relevant state
        else:
            if not iteration:
                if test_logic:
                    states = {'to_start':'Start the project',
                            'to_plan_sprint':'Make the sprint planning',
                            'to_design':'Write the design of the application',
                            'to_plan_cycle':'Choose the user stories to implement (TODO)',
                            'to_plan_code' :'Write the code plan',
                            'to_code':'Write the code of the application',
                            'to_design_tests':'Identify and design the the testcases',
                            'to_plan_tests':'Write the tests planning',
                            'to_code_tests' : 'Write the tests',
                            'to_review':'Review the code and the tests of the application',
                            'to_debug_code':'Debug the code',
                            'to_debug_tests': 'Debug the tests',
                            'to_end':'End the project'}
                
                else:
                    states = {'to_start':'Start the project',
                            'to_plan_sprint':'Make the sprint planning',
                            'to_design':'Write the design of the application',
                            'to_plan_cycle':'Choose the user stories to implement (TODO)',
                            'to_plan_code' :'Write the code plan',
                            'to_code':'Write the code of the application',
                            'to_review':'Review the code and the tests of the application',
                            'to_debug_code':'Debug the code',
                            'to_debug_tests': 'Debug the tests',
                            'to_end':'End the project'}
                    
                # Finding the last state
                index = list(states.keys()).index(state)
                
                # Creating the reduced inverted dict
                inv_states = {states[k]:k for k in list(states.keys())[:index+1]}
                
                 # Sending the state choice message
                msg = WsMessage.create_msg(object="Starting state choice",
                                        agent="Project manager",
                                        action='choice',
                                        msg_content="Please choose a starting state.",
                                        msg_sub_content=list(inv_states.keys()),
                                        document="workspace",
                                        model='')
                await websocket.send_json(msg)
                response = (await websocket.receive_json())['content']['content']
                
                # Exctracting the corresponding state keyword
                chosen_state = inv_states[response]
                
                return get_starting_message(state=chosen_state)
            # TODO : complete this part
            else:
                states = {'update_app':'Add new features into the application',
                        'update_design':'Update the design of the application',
                        'update_code':'Update the code of the application',
                        'to_review_code':'Review the code of the application',
                        'to_debug_code':'Debug the code',
                        'to_test' : 'Test the code',
                        'to_review_tests' : 'Review the code and tests',
                        'to_debug_tests':'Debug the tests',
                        'to_end':'End the project'}
                
                # Finding the last state
                index = list(states.keys()).index(state)
                
                # Creating the reduced inverted dict
                inv_states = {states[k]:k for k in list(states.keys())[:index+1]}
                
                # response = ask_user_choice(message='Choose a state to start from',
                #                         choices=list(inv_states.keys()))
                
                # Exctracting the corresponding state keyword
                chosen_state = inv_states[response]
                
                return get_starting_message(state=chosen_state)
                            
    # No problem, the folder does not exist
    else:
        state_informations = f"📁 The `{working_dir}`folder does not exist.\n"
        msg = WsMessage.create_msg(object="Project state",
                                   agent="Project manager",
                                   msg_content=state_informations,
                                   document="workspace",
                                   model='')
        await websocket.send_json(msg)
        
        return None

def identify_present_files(working_dir:str):
    """Returns a dict that contains  informations about the state of the project. If returns information for each document and None if it does not exist."""        
    present_documents = defaultdict()
    
    # Checking the request
    if os.path.exists(f"{working_dir}/infos.md"):
        infos = Document.load_informations(working_dir=working_dir)
        present_documents['request'] = infos.user_request.replace('\n',' ')
        present_documents['name'] = infos.title
        present_documents['Description'] = infos.description
    
    # Checking the sprint specification
    present_documents['backlog'] = len(os.listdir(f"{working_dir}/backlog/"))
    present_documents['requirements'] = len(os.listdir(f"{working_dir}/requirements/"))
    present_documents['current_sprint'] = len(os.listdir(f"{working_dir}/current_sprint/"))
    present_documents['done'] = len(os.listdir(f"{working_dir}/done/"))
    
    # checking the architecture
    present_documents['architecture'] = os.path.exists(f'{working_dir}/architecture.md')
    
    # checking src
    present_documents['code'] = len(os.listdir(f"{working_dir}/src")) - 1
    
    # Checking the reviews
    present_documents['reviews'] = len(os.listdir(f"{working_dir}/reviews"))
    
    # Checking the tests
    present_documents['tests'] = len(os.listdir(f"{working_dir}/tests")) -1
    
    return present_documents

def log_project_state(working_dir:str,present_doc:dict) -> str:
    """Print informations about the project and return the state of the existing project"""
    
    informations = f"📁 folder `{working_dir}` already exists, here are the documents that are already presents.\n"
    
    if 'request' in present_doc and present_doc['request'] is not None:
        informations += f"📋 User request : {present_doc['request']}\n"
    
    if 'name' in present_doc and present_doc['name'] is not None:
        informations += f"📝 Name : {present_doc['name']}\n"
    
    if 'architecture' in present_doc:
        informations += f"🏛️ Generated architecture : {present_doc['architecture']}\n"
        
    if  'backlog' in present_doc and present_doc['backlog'] > 0:
        informations += f"📄 Remaining backlog : {present_doc['backlog']}\n"
    else:
        informations += "📄 No backlog remaining\n"
        
    if 'requirements' in present_doc and present_doc['requirements']>0:
        informations += f"📄 Remaining requirements : {present_doc['requirements']}\n"
    else:
        informations += "📄 No requirements remaining\n"
    
    if 'current_sprint' in present_doc and present_doc['current_sprint']>0:
        informations += f"🏃 Items inside the last not teminated sprint : {present_doc['current_sprint']}\n"
    else:
        informations += "🏃 No sprint in progress\n"
    
    if 'done' in present_doc and present_doc['done']>0:
        informations += f"✅ Item done during last terminated sprint : {present_doc['done']}\n"
        
    if 'code' in present_doc and present_doc['code']>0:
        informations += f"📑 Number of code files generated : {present_doc['code']}\n"
        
    return informations

def get_starting_message(state:str='') -> Message:
    """Get the starting message for the application depending on the state"""
    
    # Returning the right message to the state of the project
    # Here for the first iteration
    if state=='to_start':
        return None
    elif state=='to_plan_sprint':
        return Message(object="Product_backlog_to_plan",
                       target_agent="Project_manager",
                       origin_agent="Product_owner",)
    elif state=='to_design':
        return Message(object='Planning_done',
                        target_agent='Software_architect',
                       origin_agent='Project_manager')
    elif state=='to_plan_cycle':
        return Message(object='Software_design',
                       target_agent='Project_manager',
                       origin_agent='Software_architect')
    elif state=='to_plan_code':
        return Message(object='Cycle_planned',
                       target_agent='Tech_lead',
                       origin_agent='Project_manager')
    elif state=='to_code':
        return Message(object='Code_plan',
                       target_agent='Developer',
                       origin_agent='Tech_lead',)
    elif state=='to_design_tests':
        return Message(object='Code_to_test',
                        target_agent='Tester',
                        origin_agent='Developer')
    elif state=='to_plan_tests':
        return Message(object="Testing_to_plan",
                       target_agent="Tech_lead",
                       origin_agent="Tester")
    elif state=='to_code_tests':
        return Message(object='Tests_to_write',
                       target_agent='Tester',
                       origin_agent='Tech_lead')
    elif state=='to_review':
        return Message(object='Review',
                       target_agent='Senior_developer',
                       origin_agent='Tester',)
    elif state=='to_debug_code':
        return Message(object='Code_to_debug',
                        target_agent='Developer',
                        origin_agent='Senior_developer',)
    elif state=='to_debug_tests':
        return Message(object='Tests_to_debug',
                        target_agent='Tester',
                        origin_agent='Developer',)
    elif state=='to_end':
        return Message(object='Project_completed',
                    target_agent='Product_owner',
                    origin_agent='Senior_developer')
        
    # Here for the iterations
    elif state=='update_app':
        return Message(object='Add_new_features',
                           target_agent='Product_owner',
                           origin_agent='User')
    elif state=='update_design':
        return Message(object='Planning_done_iteration',
                       origin_agent='Project_manager',
                       target_agent='Software_architect')
    else:
        return Message(object='User_request',
                       target_agent='Product_owner',
                       origin_agent='User',)
