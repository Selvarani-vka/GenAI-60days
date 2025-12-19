from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_core import Image as AGImage

from PIL import Image
from io import BytesIO
import requests
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()  # MUST be before getenv
api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(model="gpt-4.1-mini", api_key=api_key)
assistant = AssistantAgent(
    name="myAssistant",
    model_client=model_client,
    description="Assistant that can handle text and image messages",
    system_message="You are an assistant that can handle text and image messages"
)

async def textm():
    text_message = TextMessage(content="Hello, what is your name puppy?",source="user")
    result = await assistant.run(task=text_message)
    print("Text Message Response:")
    print(result.messages[-1].content)

async def imagem():
    # Fetch an image from a URL
    image_url = "https://picsum.photos/seed/picsum/200/300"
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Convert PIL Image to AGImage
    ag_image = AGImage(image)

    # Create a MultiModalMessage with the image
    multimodal_message = MultiModalMessage( content=["Here is an image for you.", ag_image],
                                           source="user")

    result = await assistant.run(task=multimodal_message)
    print("Image Message Response:")
    print(result.messages[-1].content)

async def main():
    await asyncio.gather(
        textm(),
        imagem()
    )

asyncio.run(main())