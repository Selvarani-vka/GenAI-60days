from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
import requests

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=api_key
)

def get_weather(city: str) -> str:
    """Get current weather using wttr.in (free, no API key)"""
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        forecast_today = data["weather"][0]

        return (
            f"Weather in {city}:\n"
            f"Temperature: {current['temp_C']}°C\n"
            f"Condition: {current['weatherDesc'][0]['value']}\n"
            f"Humidity: {current['humidity']}%\n"
            f"Wind: {current['windspeedKmph']} km/h\n"
            f"Today Max: {forecast_today['maxtempC']}°C, "
            f"Min: {forecast_today['mintempC']}°C"
        )

    except requests.RequestException as e:
        return f"Weather fetch failed: {e}"

assistant = AssistantAgent(
    name="toolAssistant",
    model_client=model_client,
    description="Weather assistant",
    system_message="You are a weather assistant. Use the get_weather tool when asked about weather.",
    tools=[get_weather]
)

async def main():
    report = await assistant.run(
        task="What is the weather in Erode?"
    )

    # Print final assistant reply
    print(report.messages[-1].content)

asyncio.run(main())
