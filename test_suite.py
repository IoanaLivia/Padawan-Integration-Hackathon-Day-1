#!/usr/bin/env python3
"""
Test suite for the Customer Survey Creation Tool MVP
Demonstrates various scenarios and validates functionality
"""

import subprocess
import sys
import os
import json
from datetime import datetime


def test_csv_loading():
    """Test CSV file loading functionality."""
    print("Testing CSV loading functionality...")
    
    # Test with valid CSV
    result = subprocess.run([sys.executable, 'survey_tool.py', 'sample_survey.csv'], 
                          input='quit\n', text=True, capture_output=True)
    
    if 'Loaded 4 questions' in result.stdout:
        print("✓ CSV loading test passed")
    else:
        print("✗ CSV loading test failed")
        print(result.stdout)
        print(result.stderr)
    
    # Test with non-existent file
    result = subprocess.run([sys.executable, 'survey_tool.py', 'nonexistent.csv'], 
                          text=True, capture_output=True)
    
    if 'not found' in result.stdout:
        print("✓ File not found handling test passed")
    else:
        print("✗ File not found handling test failed")
        print(result.stdout)


def test_question_types():
    """Test different question types."""
    print("\nTesting question types...")
    
    # Create a test CSV with all question types
    test_csv = """question_id,question_text,question_type,options,required
rating_test,Rate this test (1-10),rating,,true
choice_test,Choose an option,multiple_choice,Option A|Option B|Option C,true
yesno_test,Is this working?,yes_no,,true
text_test,Enter some text,text,,false"""
    
    with open('test_types.csv', 'w') as f:
        f.write(test_csv)
    
    # Test with automated responses
    responses = "5\n1\nyes\nThis is test text\n"
    result = subprocess.run([sys.executable, 'survey_tool.py', 'test_types.csv'], 
                          input=responses, text=True, capture_output=True)
    
    if 'Thank you for completing the survey!' in result.stdout:
        print("✓ All question types test passed")
    else:
        print("✗ Question types test failed")
        print(result.stdout)
        print(result.stderr)
    
    # Clean up
    if os.path.exists('test_types.csv'):
        os.remove('test_types.csv')


def test_validation():
    """Test input validation."""
    print("\nTesting input validation...")
    
    # Create a rating question CSV
    test_csv = """question_id,question_text,question_type,options,required
rating_test,Rate this (1-10),rating,,true"""
    
    with open('validation_test.csv', 'w') as f:
        f.write(test_csv)
    
    # Test invalid then valid rating
    responses = "15\nabc\n5\n"  # Invalid, invalid, valid
    result = subprocess.run([sys.executable, 'survey_tool.py', 'validation_test.csv'], 
                          input=responses, text=True, capture_output=True)
    
    if 'Please enter a number between 1 and 10' in result.stdout and 'Thank you' in result.stdout:
        print("✓ Input validation test passed")
    else:
        print("✗ Input validation test failed")
        print(result.stdout)
    
    # Clean up
    if os.path.exists('validation_test.csv'):
        os.remove('validation_test.csv')


def test_sample_generation():
    """Test sample CSV generation."""
    print("\nTesting sample CSV generation...")
    
    # Remove existing sample if present
    if os.path.exists('sample_survey.csv'):
        os.remove('sample_survey.csv')
    
    result = subprocess.run([sys.executable, 'survey_tool.py', '--create-sample'], 
                          text=True, capture_output=True)
    
    if os.path.exists('sample_survey.csv') and 'Sample CSV file created' in result.stdout:
        print("✓ Sample generation test passed")
    else:
        print("✗ Sample generation test failed")
        print(result.stdout)


def demonstrate_features():
    """Demonstrate key features of the survey tool."""
    print("\n" + "="*60)
    print("DEMONSTRATING CUSTOMER SURVEY CREATION TOOL FEATURES")
    print("="*60)
    
    print("\n1. Creating sample survey...")
    subprocess.run([sys.executable, 'survey_tool.py', '--create-sample'])
    
    print("\n2. Sample CSV content:")
    with open('sample_survey.csv', 'r') as f:
        content = f.read()
        print(content)
    
    print("\n3. Running automated survey with sample data...")
    # Simulate user responses
    responses = "9\nExcellent\nyes\nGreat tool, very user-friendly!\n"
    result = subprocess.run([sys.executable, 'survey_tool.py', 'sample_survey.csv'], 
                          input=responses, text=True, capture_output=True)
    print(result.stdout)
    
    print("\n4. Advanced survey demonstration...")
    if os.path.exists('advanced_survey.csv'):
        print("Advanced survey CSV content:")
        with open('advanced_survey.csv', 'r') as f:
            print(f.read())
        
        # Run advanced survey with responses
        adv_responses = "25-34\n8\nUser Interface\nNeed better documentation\n9\nyes\nOverall excellent experience\n"
        result = subprocess.run([sys.executable, 'survey_tool.py', 'advanced_survey.csv'], 
                              input=adv_responses, text=True, capture_output=True)
        print("\nAdvanced survey results:")
        print(result.stdout)


def main():
    """Run all tests and demonstrations."""
    print("Customer Survey Creation Tool MVP - Test Suite")
    print("=" * 60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run tests
    test_csv_loading()
    test_question_types()
    test_validation()
    test_sample_generation()
    
    # Demonstrate features
    demonstrate_features()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)
    print("\nGenerated files:")
    for file in os.listdir('.'):
        if file.endswith(('.csv', '.json')) and not file.startswith('.'):
            print(f"  - {file}")


if __name__ == '__main__':
    main()