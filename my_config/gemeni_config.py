from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
import os

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_PATH1")

gemini_client = AsyncOpenAI(api_key=key,base_url=base_url)

MODEL = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)