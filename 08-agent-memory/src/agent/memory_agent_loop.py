from models.llm_request import LLMRequest
from parser.action_parser import ActionParser

class MemoryAgentLoop:
    def __init__(self, client, tools,memory_manager,max_steps=5):
        self.client = client
        self.tools = tools
        self.memory = memory_manager
        self.max_steps = max_steps
        self.parser = ActionParser()

    def run(self, question:str):
        for step in range(self.max_steps):
            prompt = self.memory.build_context(question)
            request = LLMRequest(
                system_prompt=self.system_prompt(),
                user_prompt=prompt,
                temperature=0.2,
                max_tokens=400
            )
            response = self.client.execute(request)["output"]
            
            if "Final:" in response:
                return response

            tool_name, tool_input = self.parser.parse(response)
            tool = self.tools.get(tool_name)
            if not tool:
                continue
            observation = tool["func"](**tool_input)
            self.memory.stm.add(
                thought=response,
                action=f"{tool_name}[{tool_input}]",
                observation=observation
            )
        return "Error: Max steps reached"
    
    def system_prompt(self):
        return """
            You are a memory-aware autonomous agent.
            Use prior observations to avoid repetition.
            When you have the final answer, respond with:
            Final: [Your complete answer]   
        """