import yaml
from client.llm_client import LLMClient
from pathlib import Path

from registry.prompt_registry import PromptRegistry
from renderer.prompt_renderer import PromptRenderer
from runner.evaluation_runner import EvaluationRunner

# Pydantic settings auto-loads .env
from config import settings


def console(result):
    for version, outputs in result.items():
        print(f"Results for  {version}")
        for output in outputs:
            print(output["output"])
            print(output["latency_ms"])


if __name__ == "__main__":
    with open("datasets/cap_theorem.yaml", "r") as f:
        dataset = yaml.safe_load(f)
    registry = PromptRegistry(registry_path="../02-prompt-registry/prompts")
    renderer = PromptRenderer(registry)
    runner = EvaluationRunner(registry, renderer)
    result = runner.run(prompt_name="cap_theorem_explainer", versions=["v1", "v2"], dataset=dataset)
    console(result)
