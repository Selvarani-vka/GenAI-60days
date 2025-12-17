from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()  # MUST be before getenv

api_key = os.getenv("OPENAI_API_KEY")

# Debug check (important)
assert api_key is not None, "OPENAI_API_KEY not loaded"
async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4.1-mini", api_key=api_key)
    assistant=AssistantAgent(
        name="myAssistant",
        model_client=model_client,
        description="Assistant that shares different motivational quotes",
        system_message="You are an assistant that shares different motivational quotes"
        )
    result=await assistant.run(task="tell me a motivational quote")
    print(result.messages[-1].content)

asyncio.run(main())