import time


class PromptEvaluator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def evaluate(self, request):
        start = time.time()
        response = self.llm_client.execute(request)
        end = time.time()
        return {
            "output": response["output"],
            "usage": response["usage"],
            "latency_ms": round((end - start) * 1000, 2),
            "model": request["model"],
        }
