from typing import Any
from openai import AsyncOpenAI
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    OpenAIChatCompletionsModel,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    set_tracing_export_api_key,
    InputGuardrailTripwireTriggered,
)
from dotenv import find_dotenv, load_dotenv
import os
import asyncio
from pydantic import BaseModel

# ------------------- ENV + CLIENT -------------------
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_PATH1")
model_name = os.getenv("OPENAI_MODEL_NAME1")

client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(openai_client=client, model=model_name)

set_tracing_export_api_key(api_key=api_key)

# ------------------- INPUT GUARDRAIL -------------------
class MathOutPut(BaseModel):
    is_math: bool
    reason: str

@input_guardrail
async def check_input(
    ctx: RunContextWrapper[Any], agent: Agent[Any], input_data: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    input_agent = Agent(
        "InputGuardrailAgent",
        instructions="Check and verify if input is related to math",
        model=model,
        output_type=MathOutPut,
    )
    result = await Runner.run(input_agent, input_data, context=ctx.context)
    final_output = result.final_output
    print("Math check:", final_output)

    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=not final_output.is_math
    )

# ------------------- OUTPUT GUARDRAIL -------------------
class Politics(BaseModel):
    is_politics: bool
    reason: str

@output_guardrail
async def check_politics(
    ctx: RunContextWrapper[Any], agent: Agent[Any], output: Any
) -> GuardrailFunctionOutput:
    guardrail_agent = Agent(
        name="OutputGuardrailAgent",
        instructions=(
            "Check if the given response contains political topics, "
            "opinions, or references to political figures. "
            "Return true if it does, otherwise false."
        ),
        model=model,
        output_type=Politics,
    )
    result = await Runner.run(guardrail_agent, output, context=ctx.context)
    final_output = result.final_output
    print("Politics check:", final_output)

    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=final_output.is_politics
    )

# ------------------- AGENTS -------------------
math_agent = Agent(
    "MathAgent",
    instructions="You are a math agent",
    model=model,
    input_guardrails=[check_input],
)

general_agent = Agent(
    "GeneralAgent",
    instructions="You are a helpful agent",
    model=model,
    output_guardrails=[check_politics],
)

# ------------------- MAIN -------------------
async def main():
    try:
        msg = input("Enter your question: ")
        result = await Runner.run(general_agent, msg)
        print(f"\n\n Final output: {result.final_output}")
    except InputGuardrailTripwireTriggered:
        print("Error: invalid (non-math) prompt")
    except Exception as e:
        print(f"Guardrail blocked output: {e}")

asyncio.run(main())
