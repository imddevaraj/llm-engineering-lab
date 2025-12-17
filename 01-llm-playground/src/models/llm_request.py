from dataclasses import dataclass


@dataclass
class LLMRequest:
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    max_tokens: int = 512
    model: str = "gpt-4o-mini"
