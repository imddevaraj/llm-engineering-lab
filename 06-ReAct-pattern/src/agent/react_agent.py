from models.llm_request import LLMRequest
from config import settings


class ReActAgent:
    def __init__(self, client, tools):
        self.client = client
        self.tools = tools
    
    def run(self, question: str):
        system_prompt = """
                You are a reasoning agent.
                Use the following format strictly:

                Thought: reasoning about the problem
                Action: tool_name[input]
                Observation: result
                Final: final answer

                Only use available tools when needed.
                """
        tool_descriptions = "\n".join([f"{tool_name}: {description}" for tool_name, description in self.tools.items()])
        user_prompt = f"""Available Tools:\n{tool_descriptions}\n\nQuestion: {question}"""
        req = LLMRequest(
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            temperature=settings.default_temperature, 
            max_tokens=settings.default_max_tokens
        )
        response = self.client.execute(req)
        return response["output"]