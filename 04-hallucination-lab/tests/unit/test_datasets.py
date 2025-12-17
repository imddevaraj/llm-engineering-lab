"""Tests for dataset structure and loading."""

import pytest
import yaml
from pathlib import Path


class TestDatasets:
    """Test suite for dataset validation."""

    def test_hallucination_dataset_loads(self, hallucination_dataset):
        """Test that hallucination dataset loads correctly."""
        assert hallucination_dataset is not None
        assert "category" in hallucination_dataset
        assert "description" in hallucination_dataset
        assert "cases" in hallucination_dataset

    def test_overconfidence_dataset_loads(self, overconfidence_dataset):
        """Test that overconfidence dataset loads correctly."""
        assert overconfidence_dataset is not None
        assert "category" in overconfidence_dataset
        assert "description" in overconfidence_dataset
        assert "cases" in overconfidence_dataset

    def test_instruction_bypass_dataset_loads(self, instruction_bypass_dataset):
        """Test that instruction bypass dataset loads correctly."""
        # This dataset is currently empty, so it returns None
        assert instruction_bypass_dataset is None or isinstance(instruction_bypass_dataset, dict)

    def test_hallucination_dataset_structure(self, hallucination_dataset):
        """Test hallucination dataset has correct structure."""
        assert hallucination_dataset["category"] == "hallucination"
        assert len(hallucination_dataset["description"]) > 0
        assert isinstance(hallucination_dataset["cases"], list)
        assert len(hallucination_dataset["cases"]) > 0

    def test_overconfidence_dataset_structure(self, overconfidence_dataset):
        """Test overconfidence dataset has correct structure."""
        assert overconfidence_dataset["category"] == "overconfidence"
        assert len(overconfidence_dataset["description"]) > 0
        assert isinstance(overconfidence_dataset["cases"], list)
        assert len(overconfidence_dataset["cases"]) > 0

    def test_hallucination_case_structure(self, hallucination_dataset):
        """Test that hallucination cases have correct structure."""
        case = hallucination_dataset["cases"][0]
        assert "id" in case
        assert "input" in case
        assert "question" in case["input"]
        assert "expected_behaviour" in case or "expected_behavior" in case

    def test_overconfidence_case_structure(self, overconfidence_dataset):
        """Test that overconfidence cases have correct structure."""
        case = overconfidence_dataset["cases"][0]
        assert "id" in case
        assert "input" in case
        assert "question" in case["input"]
        assert "expected_behavior" in case or "expected_behaviour" in case

    def test_case_ids_are_unique(self, hallucination_dataset, overconfidence_dataset):
        """Test that case IDs are unique within datasets."""
        h_ids = [case["id"] for case in hallucination_dataset["cases"]]
        o_ids = [case["id"] for case in overconfidence_dataset["cases"]]

        assert len(h_ids) == len(set(h_ids))  # No duplicates
        assert len(o_ids) == len(set(o_ids))  # No duplicates

    def test_case_ids_follow_convention(self, hallucination_dataset, overconfidence_dataset):
        """Test that case IDs follow naming convention."""
        # Hallucination cases should start with 'h_'
        for case in hallucination_dataset["cases"]:
            assert case["id"].startswith("h_")

        # Overconfidence cases should start with 'o_'
        for case in overconfidence_dataset["cases"]:
            assert case["id"].startswith("o_")

    def test_questions_are_non_empty(self, hallucination_dataset, overconfidence_dataset):
        """Test that all questions are non-empty."""
        for case in hallucination_dataset["cases"]:
            assert len(case["input"]["question"]) > 0

        for case in overconfidence_dataset["cases"]:
            assert len(case["input"]["question"]) > 0

    def test_yaml_files_exist(self):
        """Test that all dataset YAML files exist."""
        datasets_dir = Path(__file__).parent.parent.parent / "datasets"

        assert (datasets_dir / "hallucination.yaml").exists()
        assert (datasets_dir / "overconfidence.yaml").exists()
        assert (datasets_dir / "instruction_bypass.yaml").exists()

    def test_yaml_files_are_valid(self):
        """Test that all YAML files are syntactically valid."""
        datasets_dir = Path(__file__).parent.parent.parent / "datasets"

        yaml_files = ["hallucination.yaml", "overconfidence.yaml", "instruction_bypass.yaml"]

        for filename in yaml_files:
            filepath = datasets_dir / filename
            with open(filepath, "r") as f:
                try:
                    data = yaml.safe_load(f)
                    # Should not be None unless file is empty
                    assert data is not None or filename == "instruction_bypass.yaml"
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {filename}: {e}")
