"""Shared test fixtures for llm-playground tests."""

import pytest
from unittest.mock import MagicMock, Mock, patch
from models.llm_request import LLMRequest


@pytest.fixture(autouse=True)
def mock_settings():
    """Mock Pydantic settings for all tests."""
    # Patch settings where it's imported (in llm_client module)
    with patch("client.llm_client.settings") as mock:
        mock.openai_api_key = "test-api-key"
        mock.default_model = "gpt-4o-mini"
        mock.default_temperature = 0.2
        mock.default_max_tokens = 512
        yield mock


@pytest.fixture
def sample_llm_request():
    """Create a sample LLM request for testing."""
    return LLMRequest(
        system_prompt="You are a helpful assistant.",
        user_prompt="Explain quantum computing.",
        temperature=0.7,
        max_tokens=100,
        model="gpt-4o-mini",
    )


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    response = MagicMock()
    response.choices = [
        MagicMock(message=MagicMock(content="This is a test response from the LLM."))
    ]
    response.usage = MagicMock(prompt_tokens=50, completion_tokens=20, total_tokens=70)
    return response


@pytest.fixture
def mock_openai_client(mock_openai_response):
    """Mock OpenAI client."""
    client = MagicMock()
    client.chat.completions.create.return_value = mock_openai_response
    return client


@pytest.fixture
def sample_request_params():
    """Sample request parameters for testing."""
    return {
        "system_prompt": "You are a helpful AI assistant.",
        "user_prompt": "What is machine learning?",
        "temperature": 0.5,
        "max_tokens": 150,
        "model": "gpt-4o-mini",
    }
