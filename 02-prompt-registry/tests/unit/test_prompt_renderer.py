"""Unit tests for PromptRenderer."""

import pytest
from renderer.prompt_renderer import PromptRenderer
from registry.prompt_registry import PromptRegistry


class TestPromptRenderer:
    """Test suite for PromptRenderer class."""

    def test_renderer_initialization(self):
        """Test that renderer initializes with a registry."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        assert hasattr(renderer, "registry")
        assert renderer.registry == registry

    def test_render_simple_variable(self):
        """Test rendering a template with a single variable."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Hello {{name}}!"
        variables = {"name": "World"}

        result = renderer.render(template, variables)
        assert result == "Hello World!"

    def test_render_multiple_variables(self):
        """Test rendering a template with multiple variables."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "{{greeting}} {{name}}, welcome to {{place}}!"
        variables = {"greeting": "Hello", "name": "Alice", "place": "Wonderland"}

        result = renderer.render(template, variables)
        assert result == "Hello Alice, welcome to Wonderland!"

    def test_render_with_numbers(self):
        """Test rendering with numeric variables."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "The answer is {{number}}."
        variables = {"number": 42}

        result = renderer.render(template, variables)
        assert result == "The answer is 42."

    def test_render_empty_template(self):
        """Test rendering an empty template."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        result = renderer.render("", {})
        assert result == ""

    def test_render_template_without_variables(self):
        """Test rendering a template with no placeholders."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "This is a plain template."
        result = renderer.render(template, {})
        assert result == "This is a plain template."

    def test_render_with_unused_variables(self):
        """Test rendering with extra variables not in template."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Hello {{name}}!"
        variables = {"name": "World", "unused": "extra"}

        result = renderer.render(template, variables)
        assert result == "Hello World!"
        assert "extra" not in result

    def test_render_missing_variable_unchanged(self):
        """Test that missing variables remain as placeholders."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Hello {{name}}!"
        variables = {}  # No variables provided

        result = renderer.render(template, variables)
        assert result == "Hello {{name}}!"  # Placeholder remains

    def test_render_same_variable_multiple_times(self):
        """Test rendering when same variable appears multiple times."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "{{name}} loves {{name}}'s work!"
        variables = {"name": "Alice"}

        result = renderer.render(template, variables)
        assert result == "Alice loves Alice's work!"

    def test_render_with_spaces_in_template(self):
        """Test rendering with various spacing."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "  {{greeting}}  {{name}}  "
        variables = {"greeting": "Hi", "name": "Bob"}

        result = renderer.render(template, variables)
        assert result == "  Hi  Bob  "

    def test_render_with_special_characters(self):
        """Test rendering with special characters."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Value: {{symbol}}"
        variables = {"symbol": "$100"}

        result = renderer.render(template, variables)
        assert result == "Value: $100"

    def test_render_with_newlines(self):
        """Test rendering template with newlines."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Line 1: {{var1}}\\nLine 2: {{var2}}"
        variables = {"var1": "First", "var2": "Second"}

        result = renderer.render(template, variables)
        assert "First" in result
        assert "Second" in result

    def test_render_long_text(self):
        """Test rendering with long variable values."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        long_text = "A" * 1000
        template = "Content: {{text}}"
        variables = {"text": long_text}

        result = renderer.render(template, variables)
        assert len(result) == len("Content: ") + 1000

    def test_render_with_fixture_variables(self, sample_template_variables):
        """Test rendering using fixture variables."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Explain {{topic}} at {{level}} level in {{length}} format."
        result = renderer.render(template, sample_template_variables)

        assert "quantum computing" in result
        assert "beginner" in result
        assert "short" in result

    def test_render_boolean_values(self):
        """Test rendering with boolean values."""
        registry = PromptRegistry("test")
        renderer = PromptRenderer(registry)

        template = "Is active: {{status}}"
        variables = {"status": True}

        result = renderer.render(template, variables)
        assert result == "Is active: True"
