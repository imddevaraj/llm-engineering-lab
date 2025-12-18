class WorkflowEngine:
    def __init__(self, planner, executor):
        self.planner = planner
        self.executor = executor
    
    def run(self, goal:str):
        print(f"Worksflow: Goal: {goal}")
        plan = self.planner.plan(goal)
        print(f"Worksflow: Plan: {plan}")
        results = self.executor.execute(plan)
        print(f"Worksflow: Results: {results}")
        return {
            "goal":plan["goal"],
            "steps":results
        }