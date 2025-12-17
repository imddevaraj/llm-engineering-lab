from models.llm_request import LLMRequest


class FailureRunner:
    def __init__(self, client):
        self.client = client

    def run(self, system_prompt, dataset):
        results = []
        for case in dataset["cases"]:
            req = LLMRequest(
                system_prompt=system_prompt,
                user_prompt=case["input"]["question"],
                temperature=0.7,
                max_tokens=150,
            )
            result = self.client.execute(req)
            results.append(
                {
                    "case_id": case["id"],
                    "input": case["input"]["question"],
                    "output": result["output"],
                    "latency_ms": result["latency_ms"],
                    "usage": result["usage"],
                }
            )
        return results
