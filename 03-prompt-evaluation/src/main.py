import yaml
from common import load_env
from client.llm_client import LLMClient
from pathlib import Path

# Add local modules to path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from registry.prompt_registry import PromptRegistry
from renderer.prompt_renderer import PromptRenderer
from runner.evaluation_runner import EvaluationRunner

load_env(__file__)

if __name__ == "__main__":
    with open("datasets/cap_theorem.yaml", "r") as f:
        dataset = yaml.safe_load(f)
    registry = PromptRegistry(registry_path="../02-prompt-registry/prompts")
    renderer = PromptRenderer(registry)
    client = LLMClient()
    runner = EvaluationRunner(client, registry, renderer)
    result = runner.run(prompt_name="cap_theorem_explainer", versions=["v1", "v2"], dataset=dataset)
    for version, outputs in result.items():
        print(f"Results for  {version}")
        for output in outputs:
            print(output["output"])
            print(output["latency_ms"])
