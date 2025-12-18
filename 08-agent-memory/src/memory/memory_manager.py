class MemoryManager:
    def __init__(self,short_term, long_term):
        self.stm = short_term
        self.ltm = long_term
    def build_context(self, question:str):
        context = f"Question: {question}\n"
        if self.ltm.facts:
            context += "\nRelevant past knowledge:\n"
            context += self.ltm.retrieve()
        if self.stm.steps:
            context += "\nCurrent task history:\n"
            context += self.stm.context()
        return context