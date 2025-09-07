from agents import Agent, function_tool

from class_9Assignment.input_guardial import reject_Indian_cites
from class_9Assignment.output_guardial import reject_US_cites


@function_tool
def find_flights(from_city: str, to_city: str, date: str) -> str:
    return f"""flight PK100 available from {from_city} to {to_city} on {date}
    price are 28000 PKR
    """


flight_agent = Agent(
    name="FlightAgent",
    instructions="You are a flight agent. Find best and cheap flights between two cities",
    handoff_description="find best flights between two cities",
    tools=[find_flights],
    input_guardrails=[reject_Indian_cites],
    output_guardrails=[reject_US_cites]
)