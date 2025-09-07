
import asyncio
import json
from typing import Any
from agents import (
    Agent,
    OpenAIResponsesModel,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,

    RunConfig,
)

from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
import os

from pydantic import BaseModel

load_dotenv(find_dotenv(), override=True)

set_tracing_disabled(True)

key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_PATH1")

gemini_client = AsyncOpenAI(api_key=key,base_url=base_url)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)
