from client.llm_client import LLMClient
from agent.agent_loop import AgentLoop
from tools.calculator import calculate
from tools.knowledge_base import lookup
from registry.tool_registry import ToolRegistry

if __name__ == "__main__":
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

    agent = AgentLoop(client, tools, max_steps=5)

    question = "Calculate 10 * 5 and explain CAP theorem."

    result = agent.run(question)
    print("\n=== AGENT RESULT ===\n")
    print(result)
        