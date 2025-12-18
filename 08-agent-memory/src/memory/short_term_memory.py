"""
Lives only during a task
 - Stores:
   - Thoughts
   - Actions
   - Observations
 - Fed back to the LLM each step
"""

class ShortTermMemory:
    def __init__(self):
        self.steps= []
    def add(self, thought, action, observation):
        self.steps.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })   
    def context(self):
        text=""
        for step in self.steps:
            text += f"""
                Thought: {step['thought']}
                Action: {step['action']}
                Observation: {step['observation']}
            """
        return text.strip()