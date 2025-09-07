

from my_config.gemeni_config import MODEL

from agents import Agent,  Runner, set_tracing_disabled


set_tracing_disabled(True)
agent: Agent = Agent(
    name="Simple Agent",
    instructions=" You are helpful agent",
    model=MODEL,
)


