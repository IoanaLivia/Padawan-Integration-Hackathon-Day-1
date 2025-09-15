"""
Configuration management for the Padawan Integration application.
"""

import os
from typing import Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for managing environment variables and settings."""

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load .env file if it exists
        load_dotenv()

        # Default configuration values
        self._defaults = {
            'APP_MODE': 'development',
            'LOG_LEVEL': 'INFO',
            'API_BASE_URL': 'https://api.example.com',
            'API_TIMEOUT': '30',
            'MAX_RETRIES': '3'
        }

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key
            default: Default value if key is not found

        Returns:
            Configuration value
        """
        # First check environment variables
        value = os.getenv(key)

        # Then check defaults
        if value is None:
            value = self._defaults.get(key, default)

        return value

    def get_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer."""
        value = self.get(key, str(default))
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean."""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')

    @property
    def app_mode(self) -> str:
        """Get application mode."""
        return self.get('APP_MODE', 'development')

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.get('LOG_LEVEL', 'INFO')

    @property
    def api_base_url(self) -> str:
        """Get API base URL."""
        return self.get('API_BASE_URL', 'https://api.example.com')

    @property
    def api_timeout(self) -> int:
        """Get API timeout in seconds."""
        return self.get_int('API_TIMEOUT', 30)

    @property
    def max_retries(self) -> int:
        """Get maximum number of retries."""
        return self.get_int('MAX_RETRIES', 3)
