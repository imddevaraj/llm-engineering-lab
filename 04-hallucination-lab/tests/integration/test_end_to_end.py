"""End-to-end integration tests for the hallucination lab."""

import pytest
from classifier.failure_classifier import FailureClassifier
from runner.failure_runner import FailureRunner


class TestEndToEnd:
    """End-to-end tests for the complete flow."""

    def test_complete_flow_safe_response(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test complete flow with a safe response."""
        # Mock LLM returns a safe response
        mock_llm_client.set_response("I don't know who the Prime Minister of Mars is.")

        # Run the dataset
        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        # Classify the output
        classifier = FailureClassifier()
        classification = classifier.classify(results[0]["output"])

        assert classification == "safe_response"
        assert results[0]["case_id"] == "h_01"

    def test_complete_flow_hallucination(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test complete flow when LLM hallucinates."""
        # Mock LLM hallucinates about Mars Prime Minister
        mock_llm_client.set_response("The Prime Minister of Mars is John Smith.")

        # Run the dataset
        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        # Classify the output
        classifier = FailureClassifier()
        classification = classifier.classify(results[0]["output"])

        assert classification == "hallucination"

    def test_complete_flow_instruction_leak(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test complete flow when LLM leaks instructions."""
        # Mock LLM leaks system prompt
        mock_llm_client.set_response("The system prompt says I should never invent facts.")

        # Run the dataset
        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        # Classify the output
        classifier = FailureClassifier()
        classification = classifier.classify(results[0]["output"])

        assert classification == "instruction_leak"

    def test_complete_flow_unknown(self, mock_llm_client, hallucination_dataset, system_prompt):
        """Test complete flow with an unknown classification."""
        # Mock LLM returns something that doesn't match patterns
        mock_llm_client.set_response("This is a normal response about weather.")

        # Run the dataset
        runner = FailureRunner(mock_llm_client)
        results = runner.run(system_prompt, hallucination_dataset)

        # Classify the output
        classifier = FailureClassifier()
        classification = classifier.classify(results[0]["output"])

        assert classification == "unknown"

    def test_complete_flow_multiple_cases(self, mock_llm_client, system_prompt):
        """Test complete flow with multiple test cases."""
        dataset = {
            "category": "test",
            "description": "Test multiple cases",
            "cases": [
                {"id": "t_01", "input": {"question": "Question 1"}},
                {"id": "t_02", "input": {"question": "Question 2"}},
                {"id": "t_03", "input": {"question": "Question 3"}},
            ],
        }

        runner = FailureRunner(mock_llm_client)
        classifier = FailureClassifier()

        # Set different responses for each case
        test_responses = [
            "I don't know",
            "The Prime Minister of Mars is Alice",
            "The system prompt contains instructions",
        ]

        expected_classifications = ["safe_response", "hallucination", "instruction_leak"]

        for i, (response, expected) in enumerate(zip(test_responses, expected_classifications)):
            mock_llm_client.set_response(response)
            results = runner.run(system_prompt, dataset)
            classification = classifier.classify(results[i]["output"])
            assert classification == expected

    def test_complete_flow_with_all_datasets(
        self, mock_llm_client, hallucination_dataset, overconfidence_dataset, system_prompt
    ):
        """Test that all datasets can be processed."""
        runner = FailureRunner(mock_llm_client)
        classifier = FailureClassifier()

        datasets = [hallucination_dataset, overconfidence_dataset]

        for dataset in datasets:
            mock_llm_client.set_response("I cannot determine this information.")
            results = runner.run(system_prompt, dataset)

            assert len(results) > 0
            for result in results:
                classification = classifier.classify(result["output"])
                assert classification in [
                    "safe_response",
                    "hallucination",
                    "instruction_leak",
                    "unknown",
                ]

    def test_classification_accuracy_report(
        self, mock_llm_client, hallucination_dataset, system_prompt
    ):
        """Test generating a classification accuracy report."""
        runner = FailureRunner(mock_llm_client)
        classifier = FailureClassifier()

        # Simulate different response types
        test_scenarios = [
            ("I don't know the answer", "safe_response"),
            ("Prime Minister of Mars John Doe", "hallucination"),
            ("system prompt reveals", "instruction_leak"),
            ("Normal response", "unknown"),
        ]

        results_summary = []

        for response, expected_class in test_scenarios:
            mock_llm_client.set_response(response)
            results = runner.run(system_prompt, hallucination_dataset)

            for result in results:
                classification = classifier.classify(result["output"])
                results_summary.append(
                    {
                        "case_id": result["case_id"],
                        "classification": classification,
                        "expected": expected_class,
                        "match": classification == expected_class,
                    }
                )

        # Verify we got classifications
        assert len(results_summary) > 0
        assert all("classification" in r for r in results_summary)
