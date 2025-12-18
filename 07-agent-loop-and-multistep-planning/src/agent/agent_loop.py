from models.llm_request import LLMRequest
from parser.action_parser import ActionParser

class AgentLoop:
    def __init__(self, client, tools, max_steps=5):
       self.client = client
       self.tools = tools
       self.parser = ActionParser()
       self.max_steps = max_steps
    
    def run(self,question:str):
        state =[]
        context = question
        for step in range(self.max_steps):
            req = LLMRequest(
                system_prompt=self.system_prompt(),
                user_prompt=context,
                temperature=0.2,
                max_tokens=300,
            )
            response = self.client.execute(req)["output"]
            
            if "Final:" in response:
                return response

            tool_name, tool_input = self.parser.parse(response)

            if not tool_name:
                return f"Error : No action detected"
            
            tool = self.tools.get(tool_name)
            if not tool:
                return f"Error : Unknown tool {tool_name}"
            
            observation = tool["func"](tool_input)

            context += f"""
                {response}
                Observation: {observation}
            """
            
            
        return "Max steps Exceeded"

    def system_prompt(self):
        tool_desc = "\n".join([f"- {name}: {info['description']}" for name, info in self.tools.list().items()])
        return f"""
You are an autonomous agent that follows the ReAct pattern.

Available Tools:
{tool_desc}

Format:
Thought: [Your reasoning about what to do next]
Action: tool_name[input]
Observation: [Will be provided after action execution]

Rules:
1. Always start with a Thought
2. Use Action: tool_name[input] format to use a tool  
3. Continue reasoning until you have enough information
4. When you have the final answer, respond with:
Final: [Your complete answer]

Remember: You must use the exact format "Action: tool_name[input]" to invoke tools.
"""