import asyncio
from agents import RunContextWrapper, Runner

# 👇 Import all your agents here
from my_agent.hotel_assistant import ask_hotel
from Weather_Info_Agent import weather_agent
from math_agent import math_agent
from simple_agent import agent

# Put all agents in a dictionary for easy lookup
AGENTS = {
    "weather": weather_agent,
    "math": math_agent,
}

async def run_agent(ctx:RunContextWrapper,agent_name: str, query: str, context: dict = None):
    """
    Runs the requested agent with the given query.
    """
    agent_name=ctx.context.get("Agents")
    if not agent_name:
        return f"❌ Unknown agent '{agent_name}'. Available: {', '.join(AGENTS.keys())}"

    agent = AGENTS[agent_name]
    result = await Runner.run(agent, query, context=context or {})
    return result.final_output


async def interactive_mode():
    """Interactive multi-agent mode"""
    print("🤖 Multi-Agent Assistant")
    print(f"Available agents: {', '.join(AGENTS.keys())}\n")

    while True:
        agent_name = input("👉 Which agent do you want to use? (type 'exit' to quit): ").strip().lower()
        if agent_name == "exit":
            break

        query = input("📝 Enter your question: ").strip()

        try:
            response = await run_agent(agent_name, query)
            print(f"\n✅ Response from {agent_name} agent:\n{response}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")


async def hotel_demo():
    """Runs demo queries for hotel assistant"""
    response1 = await ask_hotel("Hotel Sannata", "How many rooms are available?")
    print("Hotel Sannata:", response1)

    response2 = await ask_hotel("Hotel Pearl", "Who owns this hotel?")
    print("Hotel Pearl:", response2)

    response3 = await ask_hotel("Hotel GreenView", "Where is it located?")
    print("Hotel GreenView:", response3)


async def main():
     # Then start interactive mode
    print("\n💬 Switching to interactive multi-agent mode:\n")
    await interactive_mode()
    # First run hotel demo
    print("\n🏨 Running Hotel Assistant demo:\n")
    await hotel_demo()

   


if __name__ == "__main__":
    asyncio.run(main())
