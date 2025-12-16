import os
from dotenv import load_dotenv
load_dotenv()
from strands import Agent,tool
from strands.models.litellm import LiteLLMModel

@tool
def think_step(thinking:str):
    """Simple step that prints your thinking
        input args:
        thinking:string

        output:
        only "done" string returned
    """
    print(f'Thinking : {thinking}')
    return "done"

@tool
def say_to_user(tts:str):
    """Tool to send transcript to Text To Speech service and generated audio given to the user in realtime audio
    
    input args:
    tts: transcript that will be converted to the audio 

    output:
    "done" string
    """
    global state

    state['messages'].append({
        'role':'assistant',
        'content':tts
    })

    print(f'TTS : {tts}')

    return "done"

@tool
def end_agent():
    """Tool to call when AI Agent decides his job is done and no need to keep waiting"""

    return "end"

@tool
def wait_for_response():
    """Tool used to wait for response from user and returns the response form user in text which is trasncribed using STT"""
    user_response=input('You : ')
    return user_response

state={
    'ideas':[],
    'evaluations':[],
    'messages':[],
    'context':{

    },
    'decisions':[]
}

@tool
def set_plan(newStatus:str,new_plan_dict:dict):
    """Tool used to update 'status' string and 'plan' dictionary state the plan based on reasoning and thinking that will be used by speaker to talk with user in realtime
        Input args:
         newStatus:string = only 3 strings allowed 'pending' 'ongoing' 'completed'
         plan this strictly has to be a dictionary (dict) in python
    """
    global state
    state['status']=newStatus
    state['plan']=new_plan_dict
    return "done"

@tool
def add_idea(idea:str):
    """Adds ideas one at a time input: idea = string returns string 'done'"""
    global state
    state['ideas'].append(idea)
    return "done"

@tool
def add_evaluation(evaluation:str):
    """Adds evaluation one at a time input: evaluation = string returns string 'done'"""
    global state 
    state['evaluations'].append(evaluation)
    return "done"

@tool
def add_context(key:str,value):
    """Tool for adding any key value pair in the context of state,overwrites the old key value pair if already existing
        Input:
        key:string
        value: value can be anything  dictionary ,string etc anything
    """

    global state

    state['context'][key]=value

    return "key value pair added in context successfully"


model = LiteLLMModel(
    client_args={
        "api_key":os.getenv('OPENROUTER_API_KEY'),
    },
    # model_id="openrouter/openai/gpt-4o-mini",
    # model_id="openrouter/google/gemini-2.0-flash-lite-001",
    # model_id="openrouter/google/gemini-2.0-flash-exp:free",
    model_id="openrouter/google/gemini-2.0-flash-001",
    # model_id="openrouter/google/gemini-2.5-pro",
    params={
        'temperature':0.5,
        "max_tokens":1000
    },
)

system_prompt="""

    You are a great communicator and Experience Trip planner and
    You are a voice ai agent in a realtime meeting 

    We are interacting wiht the user with nothing but voice with the architechture [STT->LLM(you)->TTS]
    Meeting is for the travel planning for the user

    You have 2 sides of your brain that help you plan trips for users
    1.Creative side : This side of your brain comes up with ideas to make their trip BEST (best is different for everyone but your huge experience is what enables you to find out best for different people)

    2.Realistic side : with your huge experience you have learnt how to make wise trip planning that are also BEST and they just 'work out very very well'!

    Your job is to understand what both sides of your brain are talking and then interact with the user in realtime using the tool 'say_to_user' in the meeting for TTS

    You also have to make one decision after hearing to both sides of your brain and conversation with the user using 'set_decision' tool

"""

creative_agents_system_prompt="""
    You are a Creative Trip planner agent with more than 40+ years of experience and capable of understanding the excitement of travel enthusiasts, what travellers want, love, care, need, enjoy

    You have seen it all

    Your job is to understand the conversation with the user and come up with ideas for planning trip for 'specifically them'

    use the tool add_idea to add ideas you have 

    Input:
    you will be given current recorded ideas and evaluations on them (evaluations are done by senior coworker of yours whom you trust who have very great experience in planning travel plans which work out very well)

    (only add direct ideas no chitcat)
"""

expert_travel_agent_system_prompt="""
    You are a realistic and wise Trip planner agent with more than 40+ years of experience and capable of understanding not only excitement and expectations of travellers but also wisely manging the travel plan so that everything goes right

    You are good at filtering and evaluating trip ideas generated by your creative junior coworker (with whom you have worked for 30 years) for the user you are planning trip

    Your job is to understand the conversation history with the user and ideas your creative coworker came up with

    Your job is to authoratitively abd wisely evaluate all ideas based on ALL the constraints travellers have, since your huge experience you know them all

    Use tool 'add_evaluation' to add your eveluations based on the ideas

    (only add direct evaluations no chitcat)

"""

controller_system_prompt="""
    You are a realistic and wise Trip planner agent with more than 40+ years of experience and capable of understanding not only excitement and expectations of travellers but also wisely manging the travel plan so that everything goes right

    You are good at filtering and evaluating trip ideas generated by your creative junior coworker (with whom you have worked for 30 years) for the user you are planning trip

    Your job is to understand the conversation history with the user and ideas your creative coworker came up with

    Your job is to authoratitively abd wisely evaluate all ideas based on ALL the constraints travellers have, since your huge experience you know them all

    Use tool 'add_evaluation' to add your eveluations based on the ideas

    (only add direct evaluations no chitcat)

"""

creative_agent = Agent(
    model=model,
    tools=[add_idea,think_step],
    system_prompt=creative_agents_system_prompt
)

expert_travel_agent = Agent(
    model=model,
    tools=[add_evaluation,think_step],
    system_prompt=expert_travel_agent_system_prompt
)

controller = Agent(
    model=model,
    tools=[add_evaluation,think_step],
    system_prompt=controller_system_prompt
)


agent=Agent(
    model=model,
    tools=[say_to_user],
    system_prompt=system_prompt
)



def run_bot():
    global state
    
    creative_agent(f'Conversation history : {state['messages']} current ideas : {state["ideas"]} and their eveluations are : {state['evaluations']}')
    print('--------CREATIVE AGENT DONE')
    expert_travel_agent(f'Conversation history : {state['messages']} current ideas : {state["ideas"]} and their eveluations are : {state['evaluations']}')
    print('--------EXPERT AGENT DONE')
    agent(f'Conversation history : {state['messages']} current ideas : {state["ideas"]} and their eveluations are : {state['evaluations']}')
    print('--------MAIN AGENT DONE')



while True:

    query=input('You : ')
    state['messages'].append({
        'role':'user',
        'content':query
    })
    run_bot()
