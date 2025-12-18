class ExecutorAgent:
    def __init__(self, tools):
        self.tools = tools
    
    def execute(self, plan:dict):
        results=[]

        for step in plan['steps']:
            tool = self.tools.get(step['action'])
            if not tool:
                raise Exception(f"Unknown tool: {step['action']}")
            
            output = tool["func"](step['input'])
            results.append({
                "step_id": step['id'],
                "action": step['action'],
                "input": step['input'],
                "output": output
            })
        return results