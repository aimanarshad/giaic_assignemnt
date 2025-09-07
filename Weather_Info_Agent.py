from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
from my_config.gemeni_config import MODEL

import os
import sys

from tools.weather_tool import get_weather

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")


weather_agent: Agent = Agent(
    name="Weather Agent",
    instructions="You are an agent that tells the current weather of Karachi.",
    tools=[get_weather],  # Should be in a list
    model_settings=ModelSettings(tool_choice="auto"),
    model=MODEL
)

