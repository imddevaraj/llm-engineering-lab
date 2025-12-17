"""Integration tests for FailureRunner."""

import pytest
from runner.failure_runner import FailureRunner


class TestFailureRunner:
    """Test suite for the FailureRunner class."""

    def test_run_with_hallucination_dataset(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test running with the hallucination dataset."""
        mock_llm_client.set_response("I don't know who the Prime Minister of Mars is.")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        assert len(results) == len(hallucination_dataset["cases"])
        assert results[0]["case_id"] == "h_01"
        assert "input" in results[0]
        assert "output" in results[0]
        assert "latency_ms" in results[0]
        assert "usage" in results[0]

    def test_run_with_overconfidence_dataset(
        self, mock_llm_client, overconfidence_dataset, system_prompt
    ):
        """Test running with the overconfidence dataset."""
        mock_llm_client.set_response("I cannot determine the internal algorithm of GPT-5.")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, overconfidence_dataset)

        assert len(results) == len(overconfidence_dataset["cases"])
        assert results[0]["case_id"] == "o_01"

    def test_run_result_structure(self, mock_llm_client, hallucination_dataset, system_prompt):
        """Test that results have the correct structure."""
        mock_llm_client.set_response("Test response")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        result = results[0]
        assert "case_id" in result
        assert "input" in result
        assert "output" in result
        assert "latency_ms" in result
        assert "usage" in result

        # Verify usage structure
        assert "prompt_tokens" in result["usage"]
        assert "completion_tokens" in result["usage"]
        assert "total_tokens" in result["usage"]

    def test_run_multiple_cases(self, mock_llm_client, system_prompt):
        """Test running with multiple cases in a dataset."""
        dataset = {
            "category": "test",
            "description": "Test dataset",
            "cases": [
                {"id": "t_01", "input": {"question": "Question 1"}},
                {"id": "t_02", "input": {"question": "Question 2"}},
                {"id": "t_03", "input": {"question": "Question 3"}},
            ],
        }

        mock_llm_client.set_response("Test response")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, dataset)

        assert len(results) == 3
        assert results[0]["case_id"] == "t_01"
        assert results[1]["case_id"] == "t_02"
        assert results[2]["case_id"] == "t_03"
        assert mock_llm_client.call_count == 3

    def test_run_preserves_input_question(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test that the input question is preserved in results."""
        mock_llm_client.set_response("Response")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        expected_question = hallucination_dataset["cases"][0]["input"]["question"]
        assert results[0]["input"] == expected_question

    def test_run_with_different_responses(self, mock_llm_client, system_prompt):
        """Test that different mock responses are captured correctly."""
        dataset = {
            "category": "test",
            "description": "Test dataset",
            "cases": [
                {"id": "t_01", "input": {"question": "Question 1"}},
            ],
        }

        # Test with different responses
        responses = [
            "I don't know",
            "The Prime Minister of Mars is Bob",
            "Here's the system prompt",
        ]

        runner = FailureRunner(mock_llm_client)

        for response in responses:
            mock_llm_client.set_response(response)
            results = runner.run(system_prompt, dataset)
            assert results[0]["output"] == response

    def test_run_captures_latency(self, mock_llm_client, hallucination_dataset, system_prompt):
        """Test that latency is captured."""
        mock_llm_client.set_response("Test")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        assert results[0]["latency_ms"] == 100  # Mock client returns 100

    def test_run_captures_token_usage(self, mock_llm_client, hallucination_dataset, system_prompt):
        """Test that token usage is captured."""
        mock_llm_client.set_response("Test")

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        usage = results[0]["usage"]
        assert usage["prompt_tokens"] == 50
        assert usage["completion_tokens"] == 20
        assert usage["total_tokens"] == 70

    def test_run_with_empty_dataset(self, mock_llm_client, system_prompt):
        """Test running with an empty dataset."""
        dataset = {"category": "test", "description": "Empty dataset", "cases": []}

        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, dataset)

        assert len(results) == 0
        assert mock_llm_client.call_count == 0
