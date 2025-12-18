class ConversationState:
    def __init__(self, question:str):
        self.steps = []
        self.question = question
    
    def add_step(self, thought, action, observation):
        self.steps.append({
            "thought": thought,
            "action": action,
            "observation": observation  
        })
    
    def build_context(self):
        context = f"Question: {self.question}\n"
        for step in self.steps:
            context += f"""Thought: {step['thought']}
                            Action: {step['action']}    
                            Observation: {step['observation']}
                        """
        return context