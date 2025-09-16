#!/usr/bin/env python3
"""
Customer Survey Creation Tool MVP

A console-based Python application that creates surveys from CSV files,
collects user responses, and provides basic analysis.

Usage: python survey_tool.py <csv_file>
"""

import csv
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional


class SurveyQuestion:
    """Represents a single survey question."""
    
    def __init__(self, question_id: str, question_text: str, question_type: str, 
                 options: Optional[List[str]] = None, required: bool = True):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type.lower()
        self.options = options or []
        self.required = required
    
    def validate_response(self, response: str) -> bool:
        """Validate response based on question type."""
        if self.required and not response.strip():
            return False
            
        if self.question_type == 'multiple_choice' and response not in self.options:
            return False
        elif self.question_type == 'rating' and not response.isdigit():
            return False
        elif self.question_type == 'rating' and not (1 <= int(response) <= 10):
            return False
            
        return True


class SurveyTool:
    """Main survey tool class for processing CSV and managing surveys."""
    
    def __init__(self):
        self.questions: List[SurveyQuestion] = []
        self.responses: List[Dict[str, Any]] = []
        self.survey_title = "Customer Survey"
        
    def load_survey_from_csv(self, csv_file_path: str) -> bool:
        """Load survey questions from a CSV file."""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Expected CSV columns: question_id, question_text, question_type, options, required
                for row in reader:
                    question_id = row.get('question_id', '').strip()
                    question_text = row.get('question_text', '').strip()
                    question_type = row.get('question_type', 'text').strip()
                    options_str = row.get('options', '').strip()
                    required = row.get('required', 'true').strip().lower() == 'true'
                    
                    if not question_id or not question_text:
                        print(f"Warning: Skipping row with missing question_id or question_text")
                        continue
                    
                    # Parse options for multiple choice questions
                    options = []
                    if options_str and question_type == 'multiple_choice':
                        options = [opt.strip() for opt in options_str.split('|') if opt.strip()]
                    
                    question = SurveyQuestion(question_id, question_text, question_type, options, required)
                    self.questions.append(question)
                    
                return len(self.questions) > 0
                
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_file_path}' not found.")
            return False
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return False
    
    def display_welcome(self):
        """Display welcome message and survey instructions."""
        print("=" * 60)
        print(f"  {self.survey_title}")
        print("=" * 60)
        print("Welcome! Please answer the following questions.")
        print("Type 'quit' at any time to exit the survey.")
        print("For rating questions, use a scale of 1-10.")
        print("-" * 60)
        print()
    
    def ask_question(self, question: SurveyQuestion) -> Optional[str]:
        """Ask a single question and get user response."""
        while True:
            print(f"Question: {question.question_text}")
            
            if question.question_type == 'multiple_choice':
                print("Options:")
                for i, option in enumerate(question.options, 1):
                    print(f"  {i}. {option}")
                print("Enter the number or text of your choice:")
            elif question.question_type == 'rating':
                print("Rate from 1 to 10 (1 = lowest, 10 = highest):")
            elif question.question_type == 'yes_no':
                print("Answer with 'yes' or 'no':")
            
            response = input("> ").strip()
            
            if response.lower() == 'quit':
                return None
                
            # Handle multiple choice by number
            if question.question_type == 'multiple_choice' and response.isdigit():
                choice_num = int(response)
                if 1 <= choice_num <= len(question.options):
                    response = question.options[choice_num - 1]
            
            # Validate response
            if question.validate_response(response):
                return response
            else:
                if question.required and not response:
                    print("This question is required. Please provide an answer.")
                elif question.question_type == 'multiple_choice':
                    print("Invalid choice. Please select from the available options.")
                elif question.question_type == 'rating':
                    print("Please enter a number between 1 and 10.")
                else:
                    print("Invalid response. Please try again.")
                print()
    
    def run_survey(self) -> bool:
        """Run the complete survey process."""
        if not self.questions:
            print("Error: No questions loaded. Please load a valid CSV file.")
            return False
            
        self.display_welcome()
        
        current_responses = {}
        
        for i, question in enumerate(self.questions, 1):
            print(f"[{i}/{len(self.questions)}]")
            response = self.ask_question(question)
            
            if response is None:  # User quit
                print("\nSurvey cancelled by user.")
                return False
                
            current_responses[question.question_id] = response
            print()
        
        # Add metadata to responses
        current_responses['timestamp'] = datetime.now().isoformat()
        current_responses['completed'] = True
        
        self.responses.append(current_responses)
        
        print("=" * 60)
        print("Thank you for completing the survey!")
        print("=" * 60)
        
        return True
    
    def save_responses(self, filename: str = None) -> bool:
        """Save survey responses to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"survey_responses_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.responses, file, indent=2, ensure_ascii=False)
            print(f"Responses saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving responses: {e}")
            return False
    
    def analyze_responses(self):
        """Provide basic analysis of collected responses."""
        if not self.responses:
            print("No responses to analyze.")
            return
            
        print("\n" + "=" * 60)
        print("  SURVEY ANALYSIS")
        print("=" * 60)
        print(f"Total responses: {len(self.responses)}")
        print()
        
        # Analyze each question
        for question in self.questions:
            print(f"Question: {question.question_text}")
            print(f"Type: {question.question_type}")
            
            # Collect all responses for this question
            responses_for_question = []
            for response_set in self.responses:
                if question.question_id in response_set:
                    responses_for_question.append(response_set[question.question_id])
            
            if not responses_for_question:
                print("No responses collected.")
                print("-" * 40)
                continue
            
            if question.question_type == 'rating':
                # Calculate rating statistics
                ratings = [int(r) for r in responses_for_question if r.isdigit()]
                if ratings:
                    avg_rating = sum(ratings) / len(ratings)
                    print(f"Average rating: {avg_rating:.2f}")
                    print(f"Highest rating: {max(ratings)}")
                    print(f"Lowest rating: {min(ratings)}")
            elif question.question_type == 'multiple_choice':
                # Count occurrences of each option
                from collections import Counter
                counts = Counter(responses_for_question)
                print("Response distribution:")
                for option, count in counts.most_common():
                    percentage = (count / len(responses_for_question)) * 100
                    print(f"  {option}: {count} ({percentage:.1f}%)")
            else:
                # Display all text responses
                print("Responses:")
                for i, resp in enumerate(responses_for_question, 1):
                    print(f"  {i}. {resp}")
            
            print("-" * 40)


def create_sample_csv():
    """Create a sample CSV file for testing."""
    sample_data = [
        {
            'question_id': 'q1',
            'question_text': 'What is your overall satisfaction with our service?',
            'question_type': 'rating',
            'options': '',
            'required': 'true'
        },
        {
            'question_id': 'q2', 
            'question_text': 'Which of the following best describes your experience?',
            'question_type': 'multiple_choice',
            'options': 'Excellent|Good|Fair|Poor',
            'required': 'true'
        },
        {
            'question_id': 'q3',
            'question_text': 'Would you recommend our service to others?',
            'question_type': 'yes_no',
            'options': '',
            'required': 'true'
        },
        {
            'question_id': 'q4',
            'question_text': 'Please provide any additional comments or suggestions:',
            'question_type': 'text',
            'options': '',
            'required': 'false'
        }
    ]
    
    filename = 'sample_survey.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['question_id', 'question_text', 'question_type', 'options', 'required'])
        writer.writeheader()
        writer.writerows(sample_data)
    
    print(f"Sample CSV file created: {filename}")
    return filename


def main():
    """Main entry point for the survey tool."""
    if len(sys.argv) < 2:
        print("Usage: python survey_tool.py <csv_file>")
        print("Or use 'python survey_tool.py --create-sample' to create a sample CSV")
        sys.exit(1)
    
    if sys.argv[1] == '--create-sample':
        create_sample_csv()
        sys.exit(0)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    
    # Initialize and run survey tool
    tool = SurveyTool()
    
    if not tool.load_survey_from_csv(csv_file):
        print("Failed to load survey from CSV file.")
        sys.exit(1)
    
    print(f"Loaded {len(tool.questions)} questions from '{csv_file}'")
    
    # Run the survey
    if tool.run_survey():
        # Save responses
        tool.save_responses()
        
        # Show analysis
        tool.analyze_responses()
    
    print("Survey session completed.")


if __name__ == '__main__':
    main()