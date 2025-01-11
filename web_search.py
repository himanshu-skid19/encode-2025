from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.anthropic import Claude


web_agent = Agent(
    name="Web Agent",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)
# web_agent.print_response("Whats happening in France?", stream=True)
