"""Shared test fixtures for prompt-evaluation tests."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_llm_client():
    """Mock LLM client."""
    client = MagicMock()
    client.execute.return_value = {
        "output": "Test response",
        "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
        "latency_ms": 100,
        "model": "gpt-4o-mini",
    }
    return client


@pytest.fixture
def mock_registry():
    """Mock prompt registry."""
    registry = MagicMock()
    registry.load.return_value = {
        "system_prompt": "You are helpful.",
        "user_prompt": "Explain {{topic}}.",
        "temperature": 0.7,
        "max_tokens": 150,
    }
    return registry


@pytest.fixture
def mock_renderer():
    """Mock prompt renderer."""
    renderer = MagicMock()
    renderer.render.return_value = "Rendered prompt text"
    return renderer


@pytest.fixture
def sample_dataset():
    """Sample dataset for evaluation."""
    return {
        "cases": [
            {"input": {"topic": "AI"}},
            {"input": {"topic": "ML"}},
        ]
    }
