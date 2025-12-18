import json
from models.llm_request import LLMRequest

class PlannerAgent:
    def __init__(self, client,tools):
        self.client = client
        self.tools = tools

    
    def plan(self, goal:str):
        tool_info = "\n".join(
            f"{name}: {tool['description']}"
            for name, tool in self.tools.list().items()
        )
        system_prompt = f"""
            You are a planning agent.
            Available Tools:
            {tool_info}
            Rules:
                - The 'action' field MUST be the EXACT tool name from above  (e.g., "calculator", NOT "calculate" and "lookup", NOT "knowledge_base")
                - ONLY use the tools listed above
                - Do NOT invent tools
                - Choose the best tool for each step
                - Respond ONLY in valid JSON with:
                goal, steps[id, action, input]
            """
     
        request = LLMRequest(
            system_prompt=system_prompt,
            user_prompt=goal,
            temperature=0.2,
            max_tokens=300
        )

        response = self.client.execute(request)["output"]
        return json.loads(response)
        