"""Shared test fixtures for prompt-registry tests."""

import pytest
from unittest.mock import MagicMock, mock_open, patch
from pathlib import Path


@pytest.fixture
def sample_prompt_data():
    """Sample prompt configuration data."""
    return {
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Explain {{topic}} in simple terms.",
        "temperature": 0.7,
        "max_tokens": 150,
    }


@pytest.fixture
def mock_registry_path(tmp_path):
    """Create a temporary registry path."""
    return tmp_path / "prompts"


@pytest.fixture
def sample_template_variables():
    """Sample variables for template rendering."""
    return {"topic": "quantum computing", "level": "beginner", "length": "short"}
