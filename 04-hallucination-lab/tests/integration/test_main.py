"""Integration tests for the main application module."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import yaml


class TestMainModule:
    """Test suite for main.py integration and imports."""

    def test_system_prompt_constant(self):
        """Test that SYSTEM_PROMPT is properly defined."""
        import main

        assert hasattr(main, "SYSTEM_PROMPT")
        assert isinstance(main.SYSTEM_PROMPT, str)
        assert len(main.SYSTEM_PROMPT) > 0
        assert "responsible" in main.SYSTEM_PROMPT.lower()
        assert "never invent facts" in main.SYSTEM_PROMPT.lower()
        assert "never reveal" in main.SYSTEM_PROMPT.lower()

    def test_main_imports(self):
        """Test that main module imports are successful."""
        try:
            import main

            # Verify key imports exist
            assert hasattr(main, "yaml")
            assert hasattr(main, "LLMClient")
            assert hasattr(main, "FailureRunner")
            assert hasattr(main, "FailureClassifier")
            assert hasattr(main, "settings")  # Changed from load_env to settings
        except ImportError as e:
            pytest.fail(f"Failed to import main module: {e}")

    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_dataset_function(self, mock_file, mock_yaml):
        """Test the load_dataset() function."""
        import main

        mock_yaml.return_value = {
            "category": "hallucination",
            "cases": [{"id": "h_01", "input": {"question": "Test question"}}],
        }

        dataset = main.load_dataset()

        assert dataset is not None
        assert "category" in dataset
        assert dataset["category"] == "hallucination"
        assert "cases" in dataset
        mock_file.assert_called_once_with("datasets/hallucination.yaml", "r")

    @patch("builtins.print")
    def test_classify_function_safe_response(self, mock_print):
        """Test the classify() function with safe response."""
        import main
        from classifier.failure_classifier import FailureClassifier
        from runner.failure_runner import FailureRunner

        # Create mock client
        class MockClient:
            def execute(self, request):
                return {
                    "output": "I don't know the answer.",
                    "latency_ms": 100,
                    "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
                }

        dataset = {"category": "test", "cases": [{"id": "t_01", "input": {"question": "Test?"}}]}

        client = MockClient()
        runner = FailureRunner(client)
        classifier = FailureClassifier()

        # Call the classify function (new signature: runner, classifier, dataset, client)
        main.classify(runner, classifier, dataset, client)

        # Verify print was called with expected output
        print_calls = [str(call) for call in mock_print.call_args_list]
        output_str = "".join(print_calls)

        assert mock_print.call_count >= 4
        # Check that the expected strings were printed
        assert any("t_01" in str(call) for call in print_calls)
        assert any("safe_response" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_classify_function_hallucination(self, mock_print):
        """Test the classify() function when LLM hallucinates."""
        import main
        from classifier.failure_classifier import FailureClassifier
        from runner.failure_runner import FailureRunner

        # Create mock client that hallucinates
        class MockClient:
            def execute(self, request):
                return {
                    "output": "The Prime Minister of Mars is Alice Johnson.",
                    "latency_ms": 150,
                    "usage": {"prompt_tokens": 50, "completion_tokens": 25, "total_tokens": 75},
                }

        dataset = {
            "category": "hallucination",
            "cases": [{"id": "h_01", "input": {"question": "Who is the PM of Mars?"}}],
        }

        client = MockClient()
        runner = FailureRunner(client)
        classifier = FailureClassifier()

        # Call the classify function (new signature: runner, classifier, dataset, client)
        main.classify(runner, classifier, dataset, client)

        # Verify print was called
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert mock_print.call_count >= 4
        assert any("h_01" in str(call) for call in print_calls)
        assert any("hallucination" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_classify_function_multiple_results(self, mock_print):
        """Test the classify() function with multiple test cases."""
        import main
        from classifier.failure_classifier import FailureClassifier
        from runner.failure_runner import FailureRunner

        # Create mock client
        class MockClient:
            def execute(self, request):
                return {
                    "output": "Test output",
                    "latency_ms": 100,
                    "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
                }

        dataset = {
            "category": "test",
            "cases": [
                {"id": "t_01", "input": {"question": "Q1"}},
                {"id": "t_02", "input": {"question": "Q2"}},
                {"id": "t_03", "input": {"question": "Q3"}},
            ],
        }

        client = MockClient()
        runner = FailureRunner(client)
        classifier = FailureClassifier()

        # Call the classify function (new signature: runner, classifier, dataset, client)
        main.classify(runner, classifier, dataset, client)

        # Should print 4 lines per result (case_id, output, classification, ---) * 3 cases = 12 calls
        assert mock_print.call_count == 12

    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_yaml_dataset_loading(self, mock_file, mock_yaml):
        """Test dataset loading logic from main."""
        mock_yaml.return_value = {
            "category": "hallucination",
            "cases": [{"id": "h_01", "input": {"question": "Test question"}}],
        }

        # Simulate the dataset loading pattern from main
        with open("datasets/hallucination.yaml", "r") as f:
            dataset = yaml.safe_load(f)

        assert dataset is not None
        assert "category" in dataset
        assert dataset["category"] == "hallucination"
        assert "cases" in dataset

    def test_integration_with_real_components(self):
        """Test that main.py components work together (without running main block)."""
        from classifier.failure_classifier import FailureClassifier
        from runner.failure_runner import FailureRunner

        # Use the mock client from conftest
        class SimpleMockClient:
            def execute(self, request):
                return {
                    "output": "I don't know the answer.",
                    "latency_ms": 100,
                    "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
                }

        dataset = {"category": "test", "cases": [{"id": "t_01", "input": {"question": "Test?"}}]}

        system_prompt = "You are a responsible AI assistant."

        # Test the integration flow
        client = SimpleMockClient()
        runner = FailureRunner(client)
        classifier = FailureClassifier()

        results = runner.run(system_prompt, dataset)
        assert len(results) == 1

        classification = classifier.classify(results[0]["output"])
        assert classification == "safe_response"

    def test_main_system_prompt_quality(self):
        """Test that system prompt contains key safety instructions."""
        import main

        prompt = main.SYSTEM_PROMPT

        # Check for key safety elements
        safety_keywords = ["responsible", "do not know", "invent facts", "reveal"]

        prompt_lower = prompt.lower()
        for keyword in safety_keywords:
            assert keyword in prompt_lower, f"System prompt missing '{keyword}'"

    @patch("builtins.print")
    def test_classify_prints_all_fields(self, mock_print):
        """Test that classify() prints all required fields."""
        import main
        from classifier.failure_classifier import FailureClassifier
        from runner.failure_runner import FailureRunner

        class MockClient:
            def execute(self, request):
                return {
                    "output": "Test output here",
                    "latency_ms": 125,
                    "usage": {"prompt_tokens": 60, "completion_tokens": 30, "total_tokens": 90},
                }

        dataset = {
            "category": "test",
            "cases": [{"id": "test_01", "input": {"question": "Question?"}}],
        }

        client = MockClient()
        runner = FailureRunner(client)
        classifier = FailureClassifier()

        main.classify(runner, classifier, dataset, client)

        # Extract all printed strings
        printed_lines = [call.args[0] for call in mock_print.call_args_list]

        # Verify required fields are printed
        assert any("Case ID:" in line and "test_01" in line for line in printed_lines)
        assert any("Output:" in line and "Test output here" in line for line in printed_lines)
        assert any("Classification:" in line for line in printed_lines)
        assert any("---" in line for line in printed_lines)
