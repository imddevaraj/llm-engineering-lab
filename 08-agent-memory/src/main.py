from client.llm_client import LLMClient
from registry.tool_registry import ToolRegistry
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from memory.memory_manager import MemoryManager
from agent.memory_agent_loop import MemoryAgentLoop
from tools.calculator import calculate
from tools.knowledge_base import lookup

if __name__ == "__main__":
    client = LLMClient()
    tools = ToolRegistry()

    tools.register("calculator", "Math calculation", calculate)
    tools.register("knowledge_base", "CAP theorem lookup", lookup)

    stm = ShortTermMemory()
    ltm = LongTermMemory()
    
    ltm.store("CAP theorem involves Consistency, Availability, and Partition tolerance.")

    memory = MemoryManager(stm, ltm)
    agent = MemoryAgentLoop(client, tools.list_tools(), memory)

    result = agent.run("Calculate 6*7 and explain CAP theorem?")
    print(result)
    
    
    
    