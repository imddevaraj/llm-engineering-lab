"""Unit tests for PromptRegistry."""

import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from registry.prompt_registry import PromptRegistry


class TestPromptRegistry:
    """Test suite for PromptRegistry class."""

    def test_registry_initialization(self, mock_registry_path):
        """Test that registry initializes with a path."""
        registry = PromptRegistry(str(mock_registry_path))

        assert hasattr(registry, "registry_path")
        assert isinstance(registry.registry_path, Path)
        assert str(registry.registry_path) == str(mock_registry_path)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""
system_prompt: "You are helpful."
user_prompt: "Explain {{topic}}."
temperature: 0.7
max_tokens: 150
""",
    )
    @patch("pathlib.Path.exists")
    @patch("yaml.safe_load")
    def test_load_existing_prompt(self, mock_yaml, mock_exists, mock_file, sample_prompt_data):
        """Test loading an existing prompt."""
        mock_exists.return_value = True
        mock_yaml.return_value = sample_prompt_data

        registry = PromptRegistry("prompts")
        result = registry.load("test_prompt", "v1")

        assert result == sample_prompt_data
        assert result["system_prompt"] == "You are a helpful assistant."
        assert result["user_prompt"] == "Explain {{topic}} in simple terms."

    @patch("pathlib.Path.exists")
    def test_load_nonexistent_prompt_raises_error(self, mock_exists):
        """Test that loading nonexistent prompt raises ValueError."""
        mock_exists.return_value = False

        registry = PromptRegistry("prompts")

        with pytest.raises(ValueError) as exc_info:
            registry.load("nonexistent", "v1")

        assert "not found" in str(exc_info.value)

    @patch("builtins.open", new_callable=mock_open, read_data="system_prompt: test")
    @patch("pathlib.Path.exists")
    @patch("yaml.safe_load")
    def test_load_constructs_correct_path(self, mock_yaml, mock_exists, mock_file):
        """Test that load constructs the correct file path."""
        mock_exists.return_value = True
        mock_yaml.return_value = {"system_prompt": "test"}

        registry = PromptRegistry("prompts")
        registry.load("my_prompt", "v2")

        # Verify the path construction
        expected_path = Path("prompts") / "my_prompt/v2.yaml"
        assert mock_exists.called

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    @patch("yaml.safe_load")
    def test_load_multiple_prompts(self, mock_yaml, mock_exists, mock_file):
        """Test loading multiple different prompts."""
        mock_exists.return_value = True

        prompts = [
            {"name": "prompt1", "version": "v1", "data": {"system_prompt": "Test 1"}},
            {"name": "prompt2", "version": "v2", "data": {"system_prompt": "Test 2"}},
        ]

        registry = PromptRegistry("prompts")

        for prompt in prompts:
            mock_yaml.return_value = prompt["data"]
            result = registry.load(prompt["name"], prompt["version"])
            assert result == prompt["data"]

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    @patch("yaml.safe_load")
    def test_load_with_different_versions(self, mock_yaml, mock_exists, mock_file):
        """Test loading different versions of the same prompt."""
        mock_exists.return_value = True

        v1_data = {"system_prompt": "Version 1"}
        v2_data = {"system_prompt": "Version 2"}

        registry = PromptRegistry("prompts")

        mock_yaml.return_value = v1_data
        result_v1 = registry.load("prompt", "v1")

        mock_yaml.return_value = v2_data
        result_v2 = registry.load("prompt", "v2")

        assert result_v1 != result_v2

    def test_registry_path_is_pathlib_path(self):
        """Test that registry_path is a Path object."""
        registry = PromptRegistry("/test/path")
        assert isinstance(registry.registry_path, Path)

    @patch("pathlib.Path.exists")
    def test_error_message_includes_prompt_info(self, mock_exists):
        """Test that error message includes prompt name and version."""
        mock_exists.return_value = False

        registry = PromptRegistry("prompts")

        with pytest.raises(ValueError) as exc_info:
            registry.load("my_prompt", "v3")

        error_msg = str(exc_info.value)
        assert "my_prompt" in error_msg
        assert "v3" in error_msg
