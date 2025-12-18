import re

class ActionParser:

    def __init__(self):
        self.action_pattern = re.compile(r"Action:\s*(\w+)\[(.*)\]")
    
    def parse(self, text:str):
        match = re.search(self.action_pattern, text)
        if match:
            action_name = match.group(1)
            action_args = match.group(2)
            return action_name, action_args
        return None, None