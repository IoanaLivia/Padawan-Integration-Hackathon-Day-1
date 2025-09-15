"""
Tests for the Configuration module.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config import Config  # noqa: E402


class TestConfig:
    """Test cases for the Config class."""

    def test_default_values(self):
        """Test that default values are returned correctly."""
        config = Config()

        assert config.get('APP_MODE') == 'development'
        assert config.get('LOG_LEVEL') == 'INFO'
        assert config.get('API_BASE_URL') == 'https://api.example.com'
        assert config.get_int('API_TIMEOUT') == 30
        assert config.get_int('MAX_RETRIES') == 3

    def test_environment_override(self):
        """Test that environment variables override defaults."""
        # Set environment variable
        os.environ['APP_MODE'] = 'production'
        os.environ['API_TIMEOUT'] = '60'

        config = Config()

        assert config.get('APP_MODE') == 'production'
        assert config.get_int('API_TIMEOUT') == 60

        # Clean up
        del os.environ['APP_MODE']
        del os.environ['API_TIMEOUT']

    def test_get_with_custom_default(self):
        """Test get method with custom default value."""
        config = Config()

        result = config.get('NONEXISTENT_KEY', 'custom_default')
        assert result == 'custom_default'

    def test_get_int_conversion(self):
        """Test integer conversion."""
        config = Config()

        # Test valid integer conversion
        assert config.get_int('API_TIMEOUT') == 30

        # Test invalid integer fallback to default
        os.environ['INVALID_INT'] = 'not_a_number'
        assert config.get_int('INVALID_INT', 42) == 42

        # Clean up
        if 'INVALID_INT' in os.environ:
            del os.environ['INVALID_INT']

    def test_get_bool_conversion(self):
        """Test boolean conversion."""
        config = Config()

        # Test various true values
        for true_value in ['true', 'True', '1', 'yes', 'on']:
            os.environ['BOOL_TEST'] = true_value
            assert config.get_bool('BOOL_TEST') is True

        # Test various false values
        for false_value in ['false', 'False', '0', 'no', 'off', 'anything_else']:
            os.environ['BOOL_TEST'] = false_value
            assert config.get_bool('BOOL_TEST') is False

        # Clean up
        if 'BOOL_TEST' in os.environ:
            del os.environ['BOOL_TEST']

    def test_properties(self):
        """Test configuration properties."""
        config = Config()

        assert config.app_mode == 'development'
        assert config.log_level == 'INFO'
        assert config.api_base_url == 'https://api.example.com'
        assert config.api_timeout == 30
        assert config.max_retries == 3
