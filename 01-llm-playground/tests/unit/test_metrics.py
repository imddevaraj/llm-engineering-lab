"""Unit tests for Metrics class."""

import pytest
import time
from utils.metrics import Metrics


class TestMetrics:
    """Test suite for the Metrics class."""

    def test_metrics_initialization(self):
        """Test that metrics initializes with a start time."""
        metrics = Metrics()
        assert hasattr(metrics, "start_time")
        assert isinstance(metrics.start_time, float)

    def test_metrics_stop(self):
        """Test that stop() sets end_time."""
        metrics = Metrics()
        time.sleep(0.01)  # Small delay
        metrics.stop()

        assert hasattr(metrics, "end_time")
        assert isinstance(metrics.end_time, float)
        assert metrics.end_time > metrics.start_time

    def test_latency_ms_calculation(self):
        """Test that latency is calculated correctly."""
        metrics = Metrics()
        time.sleep(0.05)  # 50ms delay
        metrics.stop()

        latency = metrics.latency_ms()

        # Should be around 50ms (allow some variance)
        assert 40 <= latency <= 70
        assert isinstance(latency, float)

    def test_latency_ms_zero_delay(self):
        """Test latency with minimal delay."""
        metrics = Metrics()
        metrics.stop()

        latency = metrics.latency_ms()

        # Should be very small but >= 0
        assert latency >= 0
        assert latency < 10  # Less than 10ms for near-instant

    def test_latency_ms_precision(self):
        """Test that latency is rounded to 2 decimal places."""
        metrics = Metrics()
        time.sleep(0.0123)  # ~12.3ms
        metrics.stop()

        latency = metrics.latency_ms()

        # Check it's rounded to 2 decimals
        assert latency == round(latency, 2)

    def test_multiple_metrics_instances(self):
        """Test that multiple Metrics instances are independent."""
        metrics1 = Metrics()
        time.sleep(0.01)
        metrics2 = Metrics()
        time.sleep(0.01)

        metrics1.stop()
        metrics2.stop()

        latency1 = metrics1.latency_ms()
        latency2 = metrics2.latency_ms()

        # metrics1 should have higher latency
        assert latency1 > latency2

    def test_latency_with_longer_delay(self):
        """Test latency measurement with longer delay."""
        metrics = Metrics()
        time.sleep(0.1)  # 100ms
        metrics.stop()

        latency = metrics.latency_ms()

        # Should be around 100ms
        assert 90 <= latency <= 120

    def test_metrics_start_time_is_recent(self):
        """Test that start time is set to current time."""
        before = time.time()
        metrics = Metrics()
        after = time.time()

        assert before <= metrics.start_time <= after

    def test_latency_ms_returns_float(self):
        """Test that latency_ms returns a float."""
        metrics = Metrics()
        metrics.stop()
        latency = metrics.latency_ms()

        assert isinstance(latency, float)

    def test_sequential_measurements(self):
        """Test multiple sequential measurements."""
        results = []

        for _ in range(3):
            metrics = Metrics()
            time.sleep(0.01)
            metrics.stop()
            results.append(metrics.latency_ms())

        # All measurements should be positive
        assert all(r > 0 for r in results)
        # All should be similar (around 10ms each)
        assert all(5 <= r <= 20 for r in results)
