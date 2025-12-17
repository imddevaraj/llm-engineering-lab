from common import load_env
from client.llm_client import LLMClient
from models.llm_request import LLMRequest
from pathlib import Path

# Add local modules to path for registry and renderer
import sys

sys.path.insert(0, str(Path(__file__).parent))

from registry.prompt_registry import PromptRegistry
from renderer.prompt_renderer import PromptRenderer

load_env(__file__)

if __name__ == "__main__":
    PROMPT_DIR = "prompts"
    registry = PromptRegistry(registry_path=PROMPT_DIR)
    renderer = PromptRenderer(registry)
    client = LLMClient()

    prompt = registry.load("cap_theorem_explainer", "v1")

    system_prompt = prompt.get("system_prompt")
    user_prompt = renderer.render(prompt.get("user_prompt"), {"format": "3 bullet points"})

    request = LLMRequest(system_prompt=system_prompt, user_prompt=user_prompt)

    result = client.execute(request)

    print("\n--- OUTPUT ---")
    print(result["output"])
