from dotenv import load_dotenv
load_dotenv()
import os
from strands import Agent,tool
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator # Import the calculator tool

@tool
def send_message(message:str):
    """Says hello to the user
        input :
        message:string message for the user
    """

    print(f'Inside send_message : {message}')
    return "done"

model = LiteLLMModel(
    client_args={
        "api_key":os.getenv('COHERE_API_KEY')
    },
    model_id="cohere_chat/command-a-03-2025",
    params={
        'temperature':0.5,
        "max_tokens":1000
    },
)


from strands import Agent,tool
from strands.models.litellm import LiteLLMModel
model = LiteLLMModel(
    client_args={
        "api_key":os.getenv('OPENROUTER_API_KEY'),
    },
    # model_id="openrouter/openai/gpt-4o-mini",
    # model_id="openrouter/google/gemini-2.0-flash-lite-001",
    # model_id="openrouter/google/gemini-2.0-flash-exp:free",
    # model_id="openrouter/google/gemini-2.0-flash-001",
    # model_id="openrouter/google/gemini-2.5-pro",

    params={
        'temperature':0.5,
        "max_tokens":1000
    },

)
agent = Agent(
    model=model,
    tools=[send_message,calculator],
    system_prompt="You are a helpful agent. Use tools when asked (e.g., send_message to user)."
)

# OpenAI via OpenRouter (works because OpenRouter proxies OpenAI)
model_id = "openrouter/openai/gpt-4o-mini"

# Google Gemini via OpenRouter
model_id = "openrouter/google/gemini-2.5-pro"

# Cohere via OpenRouter (examples — pick exact variant OpenRouter shows)
model_id = "openrouter/cohere/command-r"
# or a precise release id you saw earlier, e.g.
model_id = "openrouter/cohere/command-a-03-2025"


import asyncio
# agent('What is 2+5 explain to a child')
# agent('Say hello to me')
# output=agent('Say hello to me')
# print(output)


async def main():
    # for event in agent.stream(
        # "Find out what is (2+3)-(4*6)/23 and send message to me"
    # ):
        # print(event)
    output = agent("Find out what is (2+3)-(4*6)/23 and send message to me")
    print(output)



if __name__ == "__main__":
    asyncio.run(main())


# main()
# for event in agent.invoke_async("Say hello to me"):
    # print(event)
# agent = Agent()

# agent("Hii")c