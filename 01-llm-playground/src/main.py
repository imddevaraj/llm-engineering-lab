from client.llm_client import LLMClient
from models.llm_request import LLMRequest
from common import load_env
load_env(__file__)
if __name__ == "__main__":
    req = LLMRequest(
        system_prompt="You are a precise assistant.",
        user_prompt="Explain CAP theorem in 3 bullet points."
    )

    client = LLMClient()
    result = client.execute(req)

    print("\n--- OUTPUT ---")
    print(result["output"])

    print("\n--- METRICS ---")
    print(f"Latency: {result['latency_ms']} ms")
    print(f"Tokens: {result['usage']}")
