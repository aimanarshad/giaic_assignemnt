from agents import Agent, ModelSettings ,set_tracing_disabled
from dotenv import load_dotenv

from my_config.gemeni_config import MODEL
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.math_tool import addition, division, subraction, multiply

load_dotenv()




math_agent:Agent = Agent(

    name = "Math Agent",
    instructions=  "You are a helpfull math agent",
    model_settings = ModelSettings(tool_choice="auto"),
    tools = [addition ,subraction , multiply , division],
    model = MODEL
)


