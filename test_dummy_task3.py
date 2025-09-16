"""
Test module for Ioana_DummyTask3

This module contains tests to validate the DummyTask3 implementation.
"""

import unittest
from dummy_task3 import greet_padawan, complete_dummy_task_3


class TestDummyTask3(unittest.TestCase):
    """Test cases for DummyTask3 functionality."""
    
    def test_greet_padawan_default(self):
        """Test greeting with default name."""
        result = greet_padawan()
        self.assertEqual(result, "Hello, Padawan! Welcome to the Integration Hackathon!")
    
    def test_greet_padawan_custom_name(self):
        """Test greeting with custom name."""
        result = greet_padawan("Ioana")
        self.assertEqual(result, "Hello, Ioana! Welcome to the Integration Hackathon!")
    
    def test_complete_dummy_task_3(self):
        """Test the main task completion function."""
        result = complete_dummy_task_3()
        
        # Verify task info structure
        self.assertIsInstance(result, dict)
        self.assertEqual(result["task_name"], "Ioana_DummyTask3")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["reference"], "AB#22812")
        self.assertEqual(result["related_work_item"], "Task 22813 IoanaDummyTask_4")
        self.assertEqual(result["message"], "Hello, Ioana! Welcome to the Integration Hackathon!")


if __name__ == "__main__":
    unittest.main()