import sys
from pathlib import Path


from client.llm_client import LLMClient
from agent.react_agent import ReActAgent
from registry.tool_registry import ToolRegistry
from tools.calculator import calculate
from tools.knowledge_base import lookup

client = LLMClient()
tools = ToolRegistry()

tools.register(
    name="calculator",
    description="Evaluate mathematical expressions",
    fn=calculate
)

tools.register(
    name="knowledge_base",
    description="Lookup basic distributed systems knowledge",
    fn=lookup
)

agent = ReActAgent(client, tools.list_tools())

question = "What is 2 + 2 * 5 and what does CAP mean?"

output = agent.run(question)
print(output)
