from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()  # MUST be before getenv
api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(model="gpt-4.1-mini", api_key=api_key)

# Single agent for reference

story_agent = AssistantAgent(
    name="multimodelAgent",
    model_client=model_client,
    description="Assistant that can write stories for children and adults",
    system_message="You are an assistant that can write stories for children and adults"
)

# async def run_story_agent():

#         task=TextMessage(
#             content="Write the story of a little girl's imaginary unicorn friend who helps her overcome her fears.", source="user")
#         result = await story_agent.run(task=task)
#         print("Final story:\n", result.messages[-1].content)

# asyncio.run(run_story_agent())

situation_agent = AssistantAgent(
    name="situationAgent",
    model_client=model_client,
    description="Assistant that can describe situations",
    system_message="You are an assistant that can describe situations vividly"
)
character_agent = AssistantAgent(
    name="characterAgent",
    model_client=model_client,
    description="Assistant that can create interesting characters",
    system_message="You are an assistant that can create interesting characters"
)

storyengine_agent = AssistantAgent(
    name="storyengineAgent",
    model_client=model_client,
    description="Assistant that can combine situation and characters to create stories",
    system_message="You are an assistant that can combine situation and characters to create stories and happy endings"
)

finalizer_agent = AssistantAgent(
    name="finalizer",
    model_client=model_client,
    system_message="""
        You are a story editor.
        Your job is to combine all previous messages into ONE coherent, complete story.
        Do not ask questions.
        Output ONLY the final story.
        """
)


team = RoundRobinGroupChat(
    [situation_agent, character_agent, storyengine_agent, finalizer_agent],
    max_turns=4
)

async def main():
    task=TextMessage(role="user", content="Write the story of a little girl's imaginary unicorn friend who helps her overcome her fears.", source="user")
    await Console(team.run_stream(task=task))

asyncio.run(main())

# async for message in team.run_stream(task=task):
# print(message)

#  from autogen_agentchat.base import TaskResult       -> This is another method,to find why the agents are stopped
#      async for message in team.run_stream(task=task):
#       if isinstance(message, TaskResult):
#            print(message.stop_reason)
#       else:
#            print(message)


