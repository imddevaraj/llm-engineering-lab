"""Unit tests for EvaluationRunner."""

import pytest
from runner.evaluation_runner import EvaluationRunner


class TestEvaluationRunner:
    """Test suite for EvaluationRunner class."""

    def test_runner_initialization(self, mock_llm_client, mock_registry, mock_renderer):
        """Test that runner initializes with all dependencies."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        assert hasattr(runner, "llm_client")
        assert hasattr(runner, "registry")
        assert hasattr(runner, "renderer")
        assert runner.llm_client == mock_llm_client
        assert runner.registry == mock_registry
        assert runner.renderer == mock_renderer

    def test_run_single_version(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test running evaluation with a single version."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        result = runner.run("test_prompt", ["v1"], sample_dataset)

        assert "v1" in result
        assert isinstance(result["v1"], list)
        assert len(result["v1"]) == 2  # Two cases in sample_dataset

    def test_run_multiple_versions(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test running evaluation with multiple versions."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        versions = ["v1", "v2", "v3"]
        result = runner.run("test_prompt", versions, sample_dataset)

        assert len(result) == 3
        for version in versions:
            assert version in result
            assert len(result[version]) == 2

    def test_run_loads_prompt_for_each_version(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that registry.load is called for each version."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        runner.run("test_prompt", ["v1", "v2"], sample_dataset)

        assert mock_registry.load.call_count == 2

    def test_run_renders_prompt_for_each_case(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that renderer.render is called for each case."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        runner.run("test_prompt", ["v1"], sample_dataset)

        # Should render for each case (2 cases)
        assert mock_renderer.render.call_count == 2

    def test_run_executes_llm_for_each_case(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that LLM client is called for each case."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        runner.run("test_prompt", ["v1"], sample_dataset)

        # Should execute for each case
        assert mock_llm_client.execute.call_count == 2

    def test_run_with_empty_dataset(self, mock_llm_client, mock_registry, mock_renderer):
        """Test running with empty dataset."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        empty_dataset = {"cases": []}
        result = runner.run("test_prompt", ["v1"], empty_dataset)

        assert "v1" in result
        assert len(result["v1"]) == 0

    def test_run_result_structure(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that result has correct structure."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        result = runner.run("test_prompt", ["v1"], sample_dataset)

        # Check result structure
        assert isinstance(result, dict)
        assert isinstance(result["v1"], list)
        first_result = result["v1"][0]
        assert "output" in first_result
        assert "usage" in first_result

    def test_run_passes_correct_parameters_to_llm(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that correct parameters are passed to LLM client."""
        mock_registry.load.return_value = {
            "system_prompt": "System",
            "user_prompt": "User {{topic}}",
            "temperature": 0.9,
            "max_tokens": 200,
        }

        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)
        runner.run("test_prompt", ["v1"], sample_dataset)

        # Verify LLM was called
        assert mock_llm_client.execute.called
        call_args = mock_llm_client.execute.call_args
        request = call_args[0][0]

        # Check request has expected attributes
        assert hasattr(request, "system_prompt")
        assert hasattr(request, "temperature")

    def test_run_with_single_case(self, mock_llm_client, mock_registry, mock_renderer):
        """Test running with a single test case."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        single_case_dataset = {"cases": [{"input": {"topic": "test"}}]}
        result = runner.run("test_prompt", ["v1"], single_case_dataset)

        assert len(result["v1"]) == 1

    def test_run_multiple_versions_independent(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that different versions produce independent results."""
        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)

        result = runner.run("test_prompt", ["v1", "v2"], sample_dataset)

        # Results should be independent
        assert result["v1"] is not result["v2"]

    def test_run_preserves_llm_output(
        self, mock_llm_client, mock_registry, mock_renderer, sample_dataset
    ):
        """Test that LLM output is preserved in results."""
        mock_llm_client.execute.return_value = {
            "output": "Specific test output",
            "usage": {},
            "latency_ms": 100,
            "model": "test-model",
        }

        runner = EvaluationRunner(mock_registry, mock_renderer, client=mock_llm_client)
        result = runner.run("test_prompt", ["v1"], sample_dataset)

        assert result["v1"][0]["output"] == "Specific test output"
