## Flowchart 
Here you can view the flowchart that illustrates the inner processes behind the application.

```mermaid
flowchart TD
    %% Requirements generation
    User(["User input"]) --> PO["Product Owner"]
    PO ==> |"Analyzes the demand \n and writes"| US("User stories and \n requirements")

    %% tech stack generation
    US ==> |"Analyzed by"| SA["Software architect"]
    SA --> |"Interprets the requirements and writes"| TC("Design")

    %% Code generation
    TC ==> |Used by| Dev[Developper]
    Dev ==> |"Writes the code"| Code("Code")
    US --> |used by| Dev

    %% Code execution and feedback
    Code ==> |Executed by| Exec["Developper\nExecutor"]
    Exec ==> |Code is OK| Tt
    Exec --> |Code is KO| Dev

    %% Tests generation
    US --> Tt
    Tt ==> |Writes| tests("Tests")
    tests ==> |Executed| TB{"Test passing ?"}
    TB --> |No| Dev
    TB ==> |Yes| PO

    PO --> |Decides the state of the project| State{End?}
    State -->|Not finished| US
    State --> |End| Product([Final Software])
    
    %% Looping
    SM["Validator"] --> |Verify conformity| US
    SM --> |Verify conformity| TC
    SM --> |Verify conformity| Code
    SM --> |Verify coverage| tests

    %% Databases
    Data1[("Software documentation database")] -.-> |RAG| PO
    Data2[("Tech Stack database")] -.-> |RAG| SA
    Data3[("Code database")] -.-> |Finetuning| Dev
    Data3 -.-> |Finetuning|Tt
```


## Class diagram

```mermaid
classDiagram
    class Agent{
        +str role
        +str tasks
        +str team_description
        +str team_goal
        
        +int max_iterations
        +Message working_message
        
        +LCRunnableAgents _agent
        +LCAgentExecutor agent
        +LCMemory memory
        +list llm
        +list tools

        +initialize_agent()
        +invoke()
        +decide_and_act()
        +receive_message()

    }


    Agent <|-- ProductOwner
    class ProductOwner{
        +int max_sprints

        +write_backlog()
        +review()
    }

    Agent <|-- SoftwareArchitect
    class SoftwareArchitect{
        +write_architecture_design()
    }

    Agent <|-- Developper
    class Developper{
        +int max_debug_try

        +write_code()
        +refine_code()
    }

    Agent <|-- DevelopperExecutor
    class DevelopperExecutor{
        +int max_debug_try

        +execute_code()
    }

    Agent <|-- Tester
    class Tester{
        +write_tests()
        +run_tests()
        +send_feedback()
    }

    Agent <|-- Validator
    class Validator{
        +check_us()
        +check_ts()
        +check_code()
        +check_tests()
    }

    Team "1" --> "1" ProductOwner
    Team "1" --> "1" SoftwareArchitect
    Team "1" --> "1" Developper
    Team "1" --> "1" Tester
    Team "1" --> "1" Validator
    class Team{
        +Dict members

        +setup()
        +run_sprints(str user_query)
        +end_sprint()
    }
    
    Team "1" --> "1" CommunicationChannel
    class CommunicationChannel{
        +list message
        +dict deliverables

        +handle_deliverable()
        +receive_message()
        +retrieve_message()
        
    }

    CommunicationChannel "1" --> "1..*" Message
    class Message{
        +str object
        +str target_agent
        +str origin_agent
        +dict content
    } 
```

## First version developpment planning

```mermaid
gantt
    title First version developpment Gantt
    dateFormat YYYY-MM-DD
    section Agents developpment 
        Agent class :a1, 2024-02-19, 7d
        Product Owner:a2, 2024-02-19, 7d
        Developper:a3, after a2, 7d
        Tester:a4, after a3, 7d

    section Interface developpment
        Project stack and setup: I1, 2024-02-15,4d
        Team orchestration: I2, 2024-02-19, 7d
        Communication interface: I3, after I2, 7d
    
    section Testing phase
        Tests: T1, after a3, 7d
    
    section Deployment
        Deployment: D1, after T1,7d
```
