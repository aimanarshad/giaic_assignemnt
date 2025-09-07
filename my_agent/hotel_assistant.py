from agents import Agent, RunContextWrapper, Runner, set_tracing_disabled
from my_config.gemeni_config import MODEL
from typing import Any

from guardrial_function.guardrial_input_function import guardrial_input_function

set_tracing_disabled(True)

# ---------------- Hotel Knowledge Base ----------------
HOTEL = {
    "Hotel Sannata": {
        "rooms_total": 200,
        "rooms_reserved": 20,
        "owner": "Mr. Ratan Lal",
        "location": "Karachi, Pakistan",
    },
    "Hotel Pearl": {
        "rooms_total": 150,
        "rooms_reserved": 10,
        "owner": "Ms. Ayesha Khan",
        "location": "Lahore, Pakistan",
    },
    "Hotel GreenView": {
        "rooms_total": 120,
        "rooms_reserved": 5,
        "owner": "Mr. Ali Raza",
        "location": "Islamabad, Pakistan",
    },
}

# ---------------- Dynamic Instruction Function ----------------
def dynamic_instruction(ctx: RunContextWrapper[Any], agent: Agent) -> str:
    hotel_name = ctx.context.get("hotel")

    if not hotel_name:
        return "You are a hotel assistant, but no hotel was provided in context."

    hotel_info = HOTEL.get(hotel_name)
    if not hotel_info:
        return f"You are a hotel assistant. The hotel '{hotel_name}' is not in our system."

    available_rooms = hotel_info["rooms_total"] - hotel_info["rooms_reserved"]

    return f"""
    You are a helpful hotel customer care assistant for {hotel_name}.
    Hotel details:
        - Hotel name: {hotel_name}
        - Location: {hotel_info['location']}
        - Total rooms: {hotel_info['rooms_total']}
        - Reserved/private rooms: {hotel_info['rooms_reserved']}
        - Available for booking: {available_rooms}
        - Owner: {hotel_info['owner']}
    """

# ---------------- Hotel Assistant Agent ----------------
hotel_assistant = Agent(
    name="Hotel Customer Care",
    instructions=dynamic_instruction,   # <-- Dynamic, not static
    model=MODEL,
    input_guardrails=[guardrial_input_function],
    output_guardrails=[],
)

# ---------------- Runner Example ----------------
async def ask_hotel(hotel: str, query: str):
    result = await Runner.run(
        hotel_assistant,
        query,
        context={"hotel": hotel},   # <-- pass hotel into context
    )
    return result.final_output
