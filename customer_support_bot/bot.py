import asyncio
import os
from dotenv import load_dotenv
from agents import (
    Agent,
    AsyncOpenAI,
    GuardrailFunctionOutput,
    ModelSettings,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    Runner,
    function_tool,
    input_guardrail,set_tracing_disabled
)
# 🔹 Load environment variables
load_dotenv()
set_tracing_disabled(True)
key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_PATH1")

# 🔹 Gemini client + model
gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)
MODEL = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

# ---------------- Fake Order DB ----------------
ORDERS_DB = {
    "123": {"status": "Shipped", "expected_delivery": "2025-09-10"},
    "456": {"status": "Processing", "expected_delivery": "2025-09-08"},
    "789": {"status": "Cancelled", "expected_delivery": None},
}

# ---------------- Function Tool ----------------
@function_tool
def get_order_status(order_id: str) -> dict:
    """Fetch order status by order ID."""
    order = ORDERS_DB.get(order_id)
    if not order:
        return {"error": f"❌ Wrong Order ID {order_id} entered."}
    return {"order_id": order_id, **order}

# ---------------- Guardrail ----------------
@input_guardrail
def check_input(ctx: RunContextWrapper, agent: Agent, input: str, query: str) -> GuardrailFunctionOutput:
    """Block rude or offensive input."""
    if "stupid" in query.lower():
        return GuardrailFunctionOutput(
            is_allowed=False,
            message="⚠️ Please ask politely.",
        )
    return GuardrailFunctionOutput(is_allowed=True)

# ---------------- Human Agent ----------------
human_agent: Agent = Agent(
    name="Human Agent",
    instructions="You are a helpful human support agent. Handle escalations politely.",
    model=MODEL,
)

# ---------------- Customer Bot Agent ----------------
customer_bot_agent: Agent = Agent(
    name="Customer Bot Agent",
    instructions=(
        "You are a customer support bot. You can:\n"
        "- Answer basic FAQs.\n"
        "- Fetch order details using tools.\n"
        "- Escalate to the Human Agent for emotional/difficult queries."
    ),
    model=MODEL,
    tools=[get_order_status],
    model_settings=ModelSettings(tool_choice="auto", metadata={"team": "customer-support"}),
    input_guardrails=[check_input],
    handoffs=[human_agent],
)

# ---------------- Runner ----------------
async def main():
    print("🤖 Customer Support Bot\n")
    while True:
        user_input = input("📝 Ask your question (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        result = await Runner.run(customer_bot_agent, user_input)
        print(f"\n✅ Response: {result.final_output}\n")

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    asyncio.run(main())
