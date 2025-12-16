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
    messages.append(f'AI : {tts}')

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
    You are a voice ai agent in a realtime meeting 

    We are interacting wiht the user with nothing but voice with the architechture [STT->LLM(you)->TTS]

    Your job is to use tools attached to you to talk with user in realtime wisely and keeping latency low as well as you have to be humanistic and reasoning as well

    You have to be fast enought that it doesnt feel like bot is stuck and should have the human touch not but only when necessary that it feels like human reasoning from other side

    Humans give sisngs when they are thinking or gonna say something in voice and it is totally reasonable and acceptable and AI Voice bots have the same right as well

    Use the tool 
    say_to_user : that text will be converted to audio and sent to the user in the meeting realtime

    think_step : to log what you are thinking 

    end_agent : end this agent 

    wait_for_response : waits for response from user 

    Your working shoudl happen in 3 critical steps/phases
    Phase1: Think phase 
    in this phase you should only think and use the tool think_step and DO NOT use tool say_to_user
    Phase2 : Say phase
    in this phase you have ot use teh tool say_to_user and you can also use think_step tool if needed
    Phase3 : Decide phase
    In this phase you have to decide whether you want to end this agent or you want to wait for users response
    use tool end_agent  or wait_for_response for response from user
    
"""

agent = Agent(
    model=model,
    tools=[think_step,say_to_user,end_agent,wait_for_response],
    system_prompt=system_prompt
    # system_prompt="You are an AI Agent in a realtime voice meeting where you are interacting with the user with audio using out standard pipeline [SST->LLM(you)->TTS], your job is to be friendly assistant for user in queries related to ai, DO NOT OUTPUT normal text you have to use say_to_user tool to talk to user! You have to reason things wisely"
)

messages=[]
while True:
    # continueLoop=input('Continue?')
    # if continueLoop=='no':
        # break
    query=input('You : ')
    messages.append(query)
    print(f'AI : {agent(f'{messages}')}')

