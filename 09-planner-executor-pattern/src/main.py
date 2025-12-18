from client.llm_client import LLMClient
from planner.planner_agent import PlannerAgent
from executor.executor_agent import ExecutorAgent
from workflow.workflow_agent import WorkflowEngine
from registry.tool_registry import ToolRegistry
from tools.calculator import calculate
from tools.knowledge_base import lookup

if __name__ == "__main__":
    llm_client = LLMClient()
    tools_registry = ToolRegistry()
   
    tools_registry.register("calculator","Math Calculation", calculate)
    tools_registry.register("knowledge_base", "CAP theorem Lookup", lookup)
    print(f"Tools registered")
 
    planner = PlannerAgent(llm_client, tools_registry)
    executor = ExecutorAgent(tools_registry)

    workflow_engine = WorkflowEngine(planner, executor)

    result = workflow_engine.run("Calculate 6 * 7 and explain CAP theorem.")
    print(result)