"""
Long-Term Memory
    - Persists across runs
    - Stores:
        - Summaries
        - Learned facts
        - Stable knowledge
"""

class LongTermMemory:
    def __init__(self):
        self.facts = []
    def store(self, fact:str):
        self.facts.append(fact)
    def retrieve(self):
        return "\n".join(self.facts)