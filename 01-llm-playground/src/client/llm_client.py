from config import settings
from openai import OpenAI
from models.llm_request import LLMRequest
from utils.metrics import Metrics


class LLMClient:
    def __init__(self):
        # Initialize OpenAI client using Pydantic settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def execute(self, request: LLMRequest):
        # Initialize enhanced metrics
        metrics = Metrics()

        # Make the API call
        response = self.client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Stop timer and record actual tokens
        metrics.stop()

        # Return comprehensive response with enhanced metrics
        return {
            "output": response.choices[0].message.content,
            "usage": response.usage,
            "latency_ms": metrics.latency_ms(),
            "model": request.model,
        }
