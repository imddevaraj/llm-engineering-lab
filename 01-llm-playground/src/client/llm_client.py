import os
from openai import OpenAI
from models.llm_request import LLMRequest
from utils.metrics import Metrics


class LLMClient:
    def __init__(self):
        # Initialize OpenAI client here (after dotenv loads in main)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
