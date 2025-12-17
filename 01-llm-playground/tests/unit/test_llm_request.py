"""Unit tests for LLMRequest dataclass."""

import pytest
from models.llm_request import LLMRequest


class TestLLMRequest:
    """Test suite for LLMRequest dataclass."""

    def test_request_initialization_with_all_params(self):
        """Test creating a request with all parameters."""
        request = LLMRequest(
            system_prompt="You are helpful.",
            user_prompt="Explain AI.",
            temperature=0.8,
            max_tokens=200,
            model="gpt-4",
        )

        assert request.system_prompt == "You are helpful."
        assert request.user_prompt == "Explain AI."
        assert request.temperature == 0.8
        assert request.max_tokens == 200
        assert request.model == "gpt-4"

    def test_request_initialization_with_defaults(self):
        """Test creating a request with default values."""
        request = LLMRequest(system_prompt="System prompt", user_prompt="User prompt")

        assert request.system_prompt == "System prompt"
        assert request.user_prompt == "User prompt"
        assert request.temperature == 0.2  # default
        assert request.max_tokens == 512  # default
        assert request.model == "gpt-4o-mini"  # default

    def test_request_partial_defaults(self):
        """Test request with some custom and some default values."""
        request = LLMRequest(
            system_prompt="Custom system", user_prompt="Custom user", temperature=0.5
        )

        assert request.temperature == 0.5
        assert request.max_tokens == 512  # default
        assert request.model == "gpt-4o-mini"  # default

    def test_request_with_fixture(self, sample_llm_request):
        """Test using the fixture."""
        assert isinstance(sample_llm_request, LLMRequest)
        assert sample_llm_request.system_prompt == "You are a helpful assistant."
        assert sample_llm_request.temperature == 0.7

    def test_request_temperature_range(self):
        """Test that temperature can be set to various values."""
        for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
            request = LLMRequest(system_prompt="Test", user_prompt="Test", temperature=temp)
            assert request.temperature == temp

    def test_request_max_tokens_values(self):
        """Test that max_tokens can be set to various values."""
        for tokens in [10, 100, 512, 1000, 4000]:
            request = LLMRequest(system_prompt="Test", user_prompt="Test", max_tokens=tokens)
            assert request.max_tokens == tokens

    def test_request_is_dataclass(self):
        """Test that LLMRequest is a dataclass."""
        request = LLMRequest(system_prompt="Test", user_prompt="Test")
        # Dataclasses have __dataclass_fields__
        assert hasattr(request, "__dataclass_fields__")

    def test_request_empty_prompts(self):
        """Test request with empty prompts (edge case)."""
        request = LLMRequest(system_prompt="", user_prompt="")
        assert request.system_prompt == ""
        assert request.user_prompt == ""

    def test_request_long_prompts(self):
        """Test request with very long prompts."""
        long_text = "A" * 10000
        request = LLMRequest(system_prompt=long_text, user_prompt=long_text)
        assert len(request.system_prompt) == 10000
        assert len(request.user_prompt) == 10000

    def test_request_special_characters(self):
        """Test request with special characters in prompts."""
        special_prompt = "Test with émojis 🎉 and spëcial çhars!"
        request = LLMRequest(system_prompt=special_prompt, user_prompt=special_prompt)
        assert request.system_prompt == special_prompt
        assert request.user_prompt == special_prompt
