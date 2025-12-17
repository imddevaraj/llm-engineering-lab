from client.llm_client import LLMClient
from models.llm_request import LLMRequest
from pathlib import Path


from registry.prompt_registry import PromptRegistry
from renderer.prompt_renderer import PromptRenderer

# Pydantic settings auto-loads .env
from config import settings


def call_llm(system_prompt, user_prompt, client: LLMClient = LLMClient()):
    request = LLMRequest(system_prompt=system_prompt, user_prompt=user_prompt)
    return client.execute(request)


def getUserPrompt(renderer, prompt):
    return renderer.render(prompt.get("user_prompt"), {"format": "3 bullet points"})


def invoke(registry, renderer, client: LLMClient = LLMClient()):
    prompt = registry.load("cap_theorem_explainer", "v1")
    system_prompt = prompt.get("system_prompt")
    user_prompt = getUserPrompt(renderer, prompt)
    return call_llm(system_prompt, user_prompt)


def console(result):
    print("\n--- OUTPUT ---")
    print(result["output"])


if __name__ == "__main__":
    PROMPT_DIR = "prompts"
    registry = PromptRegistry(registry_path=PROMPT_DIR)
    renderer = PromptRenderer(registry)
    result = invoke(registry, renderer)
    console(result)
