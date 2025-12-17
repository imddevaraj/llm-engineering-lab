"""Unit tests for LLMClient."""

import pytest
from unittest.mock import patch, MagicMock
import os
from client.llm_client import LLMClient
from models.llm_request import LLMRequest


class TestLLMClient:
    """Test suite for the LLMClient class."""

    @patch("client.llm_client.OpenAI")
    def test_client_initialization(self, mock_openai_class, mock_settings):
        """Test that LLMClient initializes with OpenAI client."""
        client = LLMClient()

        assert hasattr(client, "client")
        # Verify it was called with the mocked settings API key
        mock_openai_class.assert_called_once_with(api_key="test-api-key")

    @patch("client.llm_client.OpenAI")
    def test_execute_basic_request(
        self, mock_openai_class, sample_llm_request, mock_openai_response
    ):
        """Test executing a basic LLM request."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        client = LLMClient()
        result = client.execute(sample_llm_request)

        # Verify API was called
        mock_client_instance.chat.completions.create.assert_called_once()

        # Verify result structure
        assert "output" in result
        assert "usage" in result
        assert "latency_ms" in result
        assert "model" in result

    @patch("client.llm_client.OpenAI")
    def test_execute_returns_correct_output(self, mock_openai_class, mock_openai_response):
        """Test that execute returns the correct output text."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(system_prompt="Test system", user_prompt="Test user")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        assert result["output"] == "This is a test response from the LLM."

    @patch("client.llm_client.OpenAI")
    def test_execute_includes_usage_metrics(self, mock_openai_class, mock_openai_response):
        """Test that usage metrics are included in response."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(system_prompt="Test", user_prompt="Test")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        usage = result["usage"]
        assert usage.prompt_tokens == 50
        assert usage.completion_tokens == 20
        assert usage.total_tokens == 70

    @patch("client.llm_client.OpenAI")
    def test_execute_includes_latency(self, mock_openai_class, mock_openai_response):
        """Test that latency is measured and included."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(system_prompt="Test", user_prompt="Test")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        assert "latency_ms" in result
        assert isinstance(result["latency_ms"], float)
        assert result["latency_ms"] >= 0

    @patch("client.llm_client.OpenAI")
    def test_execute_includes_model(self, mock_openai_class, mock_openai_response):
        """Test that model name is included in response."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(system_prompt="Test", user_prompt="Test", model="gpt-4")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        assert result["model"] == "gpt-4"

    @patch("client.llm_client.OpenAI")
    def test_execute_with_custom_parameters(self, mock_openai_class, mock_openai_response):
        """Test execute with custom temperature and max_tokens."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(
            system_prompt="Test", user_prompt="Test", temperature=0.9, max_tokens=1000
        )

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        # Verify API was called with correct parameters
        call_args = mock_client_instance.chat.completions.create.call_args
        assert call_args.kwargs["temperature"] == 0.9
        assert call_args.kwargs["max_tokens"] == 1000

    @patch("client.llm_client.OpenAI")
    def test_execute_passes_correct_messages(self, mock_openai_class, mock_openai_response):
        """Test that execute passes correct message format to API."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        request = LLMRequest(system_prompt="You are helpful.", user_prompt="Explain AI.")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()
            result = client.execute(request)

        # Verify messages structure
        call_args = mock_client_instance.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are helpful."
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Explain AI."

    @patch("client.llm_client.OpenAI")
    def test_execute_multiple_requests(self, mock_openai_class, mock_openai_response):
        """Test executing multiple requests with same client."""
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = LLMClient()

            # Execute multiple requests
            for i in range(3):
                request = LLMRequest(system_prompt=f"System {i}", user_prompt=f"User {i}")
                result = client.execute(request)
                assert "output" in result

        # Verify API was called 3 times
        assert mock_client_instance.chat.completions.create.call_count == 3
