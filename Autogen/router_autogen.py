from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
router_api_key=os.getenv("OPENROUTER_API_KEY")

open_router_client=OpenAIChatCompletionClient(
    base_url='https://openrouter.ai/api/v1',
    api_key=router_api_key,
    model='nvidia/nemotron-3-nano-30b-a3b:free',
    model_info={
        "family": "nemotron-3",
        "vision": False,
        "function_calling": False,
        "json_output": "best_effort"
    }
    )
assistant=AssistantAgent(
    name="MyAssist",
    model_client=open_router_client,
    system_message="you are a helpful assistant"
)
async def chat(question):
    result= await assistant.run(task=question)
    print(result.messages[-1].content)

asyncio.run(chat("Tell me about Tamil history"))