import yaml
from pathlib import Path


class PromptRegistry:
    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)

    def load(self, prompt_name: str, version: str):
        prompt_file = self.registry_path / f"{prompt_name}/{version}.yaml"
        if not prompt_file.exists():
            raise ValueError(f"Prompt {prompt_name}/{version} not found")
        with open(prompt_file, "r") as f:
            prompt_data = yaml.safe_load(f)
        return prompt_data
