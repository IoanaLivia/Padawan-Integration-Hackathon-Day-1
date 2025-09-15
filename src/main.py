#!/usr/bin/env python3
"""
Padawan Integration Hackathon - Day 1 Application
A simple demonstration of integration patterns and best practices.
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from integrations.api_client import APIClient  # noqa: E402
from utils.config import Config  # noqa: E402
from utils.logger import setup_logger  # noqa: E402


def main():
    """Main application entry point."""
    # Setup logging
    logger = setup_logger()

    # Load configuration
    config = Config()

    logger.info("🚀 Starting Padawan Integration Hackathon Application")
    logger.info(f"Application mode: {config.get('APP_MODE', 'development')}")

    # Initialize API client
    api_client = APIClient(config)

    # Demonstrate basic functionality
    try:
        # Test API connectivity
        logger.info("Testing API connectivity...")
        status = api_client.health_check()

        if status.get('healthy', False):
            logger.info("✅ API connectivity test passed")
        else:
            logger.warning("⚠️ API connectivity test failed")

        # Demonstrate integration patterns
        logger.info("Demonstrating integration patterns...")

        # Example: Fetch and process data
        sample_data = api_client.fetch_sample_data()
        if sample_data:
            logger.info(f"📊 Fetched sample data: {len(sample_data.get('items', []))} items")

        # Example: Process integration event
        event_result = api_client.process_integration_event({
            'type': 'hackathon_demo',
            'source': 'padawan_app',
            'timestamp': '2024-01-01T00:00:00Z',
            'data': {'message': 'Hello from Padawan Integration!'}
        })

        if event_result.get('success', False):
            logger.info("✅ Integration event processed successfully")

        logger.info("🎉 Application completed successfully!")

    except Exception as e:
        logger.error(f"❌ Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
