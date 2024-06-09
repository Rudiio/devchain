from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from devchain.team import Team
from devchain.communication.message import Message
from devchain.communication.WSMessage import WsMessage
from devchain.utils.project_load import identify_existing_project

app = FastAPI()

# Define a WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Waiting to connect to the client
    await websocket.accept()
    
    try:
        await server_dev(websocket=websocket)
    except WebSocketDisconnect:
        print("The Client disconected.")
    
async def server_dev(test_logic : bool = False,
                     websocket : WebSocket = None) -> None:
    """Launch the development of a new project"""

    # Send first message to confirm connection
    # It should wait for a message with a folder
    msg = WsMessage.create_msg(object='startup',
                                agent='Project manager',
                                msg_content='Please select a project workspace.',
                                document='workspace',
                                model='',)
    await websocket.send_json(data=msg)
    
    # Receiving the response
    response = await websocket.receive_json()
    workspace = response['content']['content']
    
    # Launching the identification of the project
    starting_message = await identify_existing_project(working_dir=workspace,
                                                       websocket=websocket,
                                                       test_logic=test_logic)
    
    # No message, so starting from the beginning
    if starting_message is None:
        msg = WsMessage.create_msg(object='startup',
                                   agent='Project manager',
                                   msg_content='Describe precisely the application that you want to develop. Give a comprehensive explanation of the features and functionalities along with technical details.',
                                   document='workspace',
                                   model='',)
        await websocket.send_json(data=msg)
        user_demand = (await websocket.receive_json())['content']['content']
        
        starting_message = Message(object='User_request',
                          target_agent='Product_owner',
                          origin_agent='User')
        
    # Message so starting from the previous state
    else:
        user_demand = ''
    
    # Creating the team (not the environment)    
    team = Team.from_config(working_dir=workspace,websocket=websocket)
    
    # Starting the development from the message
    await team.start(request=user_demand,message=starting_message)
    
    await team.run_sprint()

    