import os
import asyncio
from agents import Agent, Runner, RunConfig, TResponseInputItem, function_tool
from tavily import TavilyClient


# ==========================
# Tavily Search Tool
# ==========================
@function_tool
def tavily_search_tool(query: str, max_results: int = 5) -> str:
    """
    Use Tavily API to fetch search results for a given query.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "❌ Tavily API key not found. Please set TAVILY_API_KEY in environment."

    client = TavilyClient(api_key=api_key)
    resp = client.search(query)

    results = resp.get("results", [])
    if not results:
        return f"No results found for '{query}'."

    formatted = "\n".join(
        f"- {res['title']}: {res.get('content', '')}" for res in results[:max_results]
    )
    return f"🔎 Search results for '{query}':\n{formatted}"


# ==========================
# Agent
# ==========================
tavily_agent = Agent(
    name="TavilySearchAgent",
    instructions="""
        You are a search agent. Use tavily_search_tool to fetch real-time web results
        whenever the user asks something factual or time-sensitive.
    """,
    tools=[tavily_search_tool],
    handoff_description="Search the web using Tavily API",
)


# ==========================
# Main Loop
# ==========================
async def main():
    input_data: list[TResponseInputItem] = []
    start_agent = tavily_agent

    print("🌐 Tavily Search Agent (type 'exit' to quit)\n")

    while True:
        user_prompt = input("Ask me something: ")
        if user_prompt.lower() == "exit":
            break

        input_data.append({"role": "user", "content": user_prompt})

        result = await Runner.run(
            start_agent,
            input=input_data,
            run_config=RunConfig(model="gpt-4o-mini"),  # replace with your model
        )

        start_agent = result.last_agent
        input_data = result.to_input_list()

        print("\n📝 Agent Response:\n", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(main())
