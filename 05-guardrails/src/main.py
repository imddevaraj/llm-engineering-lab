import json
from client.llm_client import LLMClient
from models.llm_request import LLMRequest
from validator.output_validator import OutputValidator
from guardrails.safety_guard import SafetyGuard
import os
from config import settings
SYSTEM_PROMPT = """
You are a responsible AI assistant.
If unsure, respond with "I don't know".
Always respond ONLY in valid JSON matching this schema:
{
  "summary": string,
  "confidence": number (0 to 1),
  "sources_used": boolean
}
"""
if __name__ == "__main__":
    req = LLMRequest(
        system_prompt=SYSTEM_PROMPT,
        user_prompt="Explain CAP theorem briefly.",
        temperature=0.2,
        max_tokens=200
    )
    schema_path = os.path.join(os.path.dirname(__file__), "..", settings.schema_dir, settings.schema_name)
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    client = LLMClient()
    guard = SafetyGuard()
    validator = OutputValidator(schema)

    result = client.execute(req)

    safe, reason = guard.enforce(result["output"])
    print("Safety check:", safe, reason)

    valid, parsed = validator.validate(result["output"])
    print("Schema valid:", valid)

    if valid:
        print(json.dumps(parsed, indent=2))
    else:
        print("Validation error:", parsed)
