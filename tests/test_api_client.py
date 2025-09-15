"""
Tests for the API Client module.
"""

import sys
from pathlib import Path
import pytest

# Add src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from integrations.api_client import APIClient  # noqa: E402
from utils.config import Config  # noqa: E402


class TestAPIClient:
    """Test cases for the APIClient class."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        return Config()

    @pytest.fixture
    def api_client(self, config):
        """Create an API client instance for testing."""
        return APIClient(config)

    def test_health_check(self, api_client):
        """Test the health check functionality."""
        result = api_client.health_check()

        assert isinstance(result, dict)
        assert 'healthy' in result
        assert 'status' in result
        assert 'timestamp' in result
        assert result['healthy'] is True
        assert result['status'] == 'ok'

    def test_fetch_sample_data(self, api_client):
        """Test fetching sample data."""
        result = api_client.fetch_sample_data()

        assert result is not None
        assert isinstance(result, dict)
        assert 'items' in result
        assert 'total' in result
        assert 'timestamp' in result
        assert len(result['items']) == 3
        assert result['total'] == 3

    def test_process_integration_event_valid(self, api_client):
        """Test processing a valid integration event."""
        event = {
            'type': 'test_event',
            'source': 'test_source',
            'timestamp': '2024-01-01T00:00:00Z',
            'data': {'key': 'value'}
        }

        result = api_client.process_integration_event(event)

        assert isinstance(result, dict)
        assert result['success'] is True
        assert 'event_id' in result
        assert 'processed_at' in result
        assert 'message' in result

    def test_process_integration_event_invalid(self, api_client):
        """Test processing an invalid integration event."""
        event = {
            'type': 'test_event'
            # Missing required fields
        }

        result = api_client.process_integration_event(event)

        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'error' in result
        assert 'timestamp' in result

    def test_send_notification(self, api_client):
        """Test sending a notification."""
        result = api_client.send_notification("Test message", "test_channel")

        assert result is True

    def test_send_notification_default_channel(self, api_client):
        """Test sending a notification with default channel."""
        result = api_client.send_notification("Test message")

        assert result is True
