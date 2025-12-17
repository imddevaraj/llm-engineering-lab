from models.llm_request import LLMRequest


class EvaluationRunner:
    def __init__(self, client, registry, renderer):
        self.llm_client = client
        self.registry = registry
        self.renderer = renderer

    def run(self, prompt_name: str, versions, dataset):
        result = {}
        for version in versions:
            prompt = self.registry.load(prompt_name, version)
            version_result = []
            for case in dataset["cases"]:
                user_prompt = self.renderer.render(prompt.get("user_prompt"), case["input"])
                request = LLMRequest(
                    system_prompt=prompt.get("system_prompt"),
                    user_prompt=user_prompt,
                    temperature=prompt.get("temperature"),
                    max_tokens=prompt.get("max_tokens"),
                )
                output = self.llm_client.execute(request)
                version_result.append(output)
            result[version] = version_result
        return result
