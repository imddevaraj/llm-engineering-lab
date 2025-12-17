class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, name: str, description: str, fn: callable):
        self.tools[name] = {
            "description": description,
            "func": fn
        }
    
    def get(self, name: str):
        return self.tools.get(name)

    def list(self):
        return self.tools
    
    def list_tools(self):
        """Return dictionary of tool names and descriptions for agent."""
        return {name: info["description"] for name, info in self.tools.items()}