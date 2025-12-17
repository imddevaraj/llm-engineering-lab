from client.llm_client import LLMClient
from models.llm_request import LLMRequest
from config import settings  # Pydantic settings auto-loads .env


def call_llm(system_prompt, user_prompt, client: LLMClient = LLMClient()):
    request = LLMRequest(system_prompt=system_prompt, user_prompt=user_prompt)
    return client.execute(request)


def console(result):

    print("\n--- OUTPUT ---")
    print(result["output"])

    print("\n--- METRICS ---")
    print(f"Latency: {result['latency_ms']} ms")
    print(f"Tokens: {result['usage']}")


if __name__ == "__main__":
    output = call_llm(
        system_prompt="You are a precise assistant.",
        user_prompt="Explain CAP theorem in 3 bullet points.",
    )

    console(output)
