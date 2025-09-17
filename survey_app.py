#!/usr/bin/env python3
"""
Customer Survey Creation Tool MVP
A console-based Python application that reads survey questions from a CSV file
and conducts interactive surveys with users.
"""

import csv
import sys
import os
from typing import List, Dict, Any
from datetime import datetime


class SurveyQuestion:
    """Represents a single survey question."""
    
    VALID_TYPES = {'text', 'number', 'multiple_choice', 'yes_no'}
    
    def __init__(self, question_id: str, question_text: str, question_type: str, options: str = ""):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type.lower() if question_type else 'text'
        
        # Validate question type
        if self.question_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid question type '{question_type}'. Valid types: {', '.join(self.VALID_TYPES)}")
            
        self.options = self._parse_options(options) if options else []
        
        # Validate that multiple choice questions have options
        if self.question_type == 'multiple_choice' and not self.options:
            raise ValueError(f"Multiple choice question '{question_id}' must have options")
    
    def _parse_options(self, options_str: str) -> List[str]:
        """Parse options from comma-separated string."""
        return [option.strip() for option in options_str.split(',') if option.strip()]
    
    def validate_response(self, response: str) -> bool:
        """Validate user response based on question type."""
        if self.question_type == "text":
            return len(response.strip()) > 0
        elif self.question_type == "number":
            try:
                float(response)
                return True
            except ValueError:
                return False
        elif self.question_type == "multiple_choice":
            try:
                choice_num = int(response)
                return 1 <= choice_num <= len(self.options)
            except ValueError:
                return False
        elif self.question_type == "yes_no":
            return response.lower() in ['y', 'yes', 'n', 'no']
        return True


class SurveyApp:
    """Main survey application class."""
    
    def __init__(self):
        self.questions: List[SurveyQuestion] = []
        self.responses: Dict[str, Any] = {}
        self.survey_name = ""
    
    def load_survey_from_csv(self, csv_file_path: str) -> bool:
        """Load survey questions from CSV file."""
        if not os.path.exists(csv_file_path):
            print(f"Error: CSV file '{csv_file_path}' not found.")
            return False
        
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate required columns
                required_columns = ['question_id', 'question_text', 'question_type']
                if not all(col in reader.fieldnames for col in required_columns):
                    print("Error: CSV file must contain columns: question_id, question_text, question_type")
                    return False
                
                for row in reader:
                    # Skip rows with missing essential data
                    if not row.get('question_id') or not row.get('question_text'):
                        print(f"Warning: Skipping row with missing question_id or question_text")
                        continue
                    
                    try:
                        question = SurveyQuestion(
                            question_id=row['question_id'],
                            question_text=row['question_text'],
                            question_type=row.get('question_type', 'text'),
                            options=row.get('options', '')
                        )
                        self.questions.append(question)
                    except ValueError as e:
                        print(f"Error loading question '{row.get('question_id', 'unknown')}': {e}")
                        continue
            
            self.survey_name = os.path.splitext(os.path.basename(csv_file_path))[0]
            print(f"Successfully loaded {len(self.questions)} questions from '{csv_file_path}'")
            return True
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return False
    
    def display_question(self, question: SurveyQuestion) -> None:
        """Display a question to the user."""
        print(f"\n{question.question_text}")
        
        if question.question_type == "multiple_choice" and question.options:
            print("Options:")
            for i, option in enumerate(question.options, 1):
                print(f"  {i}. {option}")
            print("Enter the number of your choice:")
        elif question.question_type == "yes_no":
            print("Enter 'y' for Yes or 'n' for No:")
        elif question.question_type == "number":
            print("Enter a number:")
        else:
            print("Enter your response:")
    
    def get_user_response(self, question: SurveyQuestion) -> str:
        """Get and validate user response for a question."""
        while True:
            self.display_question(question)
            response = input("> ").strip()
            
            if not response:
                print("Please provide a response.")
                continue
            
            if question.validate_response(response):
                # Convert response to appropriate format
                if question.question_type == "number":
                    return str(float(response))
                elif question.question_type == "multiple_choice":
                    choice_index = int(response) - 1
                    return question.options[choice_index]
                elif question.question_type == "yes_no":
                    return "Yes" if response.lower() in ['y', 'yes'] else "No"
                else:
                    return response
            else:
                print("Invalid response. Please try again.")
    
    def conduct_survey(self) -> bool:
        """Conduct the survey by presenting questions to the user."""
        if not self.questions:
            print("No questions loaded. Please load a CSV file first.")
            return False
        
        print(f"\n{'='*50}")
        print(f"Welcome to the {self.survey_name.replace('_', ' ').title()} Survey!")
        print(f"{'='*50}")
        print("Please answer the following questions:")
        
        for i, question in enumerate(self.questions, 1):
            print(f"\nQuestion {i} of {len(self.questions)}")
            print("-" * 30)
            
            response = self.get_user_response(question)
            self.responses[question.question_id] = {
                'question': question.question_text,
                'response': response,
                'question_type': question.question_type
            }
        
        print(f"\n{'='*50}")
        print("Thank you for completing the survey!")
        print(f"{'='*50}")
        return True
    
    def display_summary(self) -> None:
        """Display a summary of responses."""
        if not self.responses:
            print("No responses to display.")
            return
        
        print(f"\n{'='*50}")
        print("SURVEY SUMMARY")
        print(f"{'='*50}")
        print(f"Survey: {self.survey_name.replace('_', ' ').title()}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Questions: {len(self.responses)}")
        print(f"{'='*50}")
        
        for question_id, data in self.responses.items():
            print(f"\n{data['question']}")
            print(f"Response: {data['response']}")
    
    def save_responses(self, output_file: str = None) -> bool:
        """Save responses to a CSV file."""
        if not self.responses:
            print("No responses to save.")
            return False
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{self.survey_name}_responses_{timestamp}.csv"
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['question_id', 'question', 'response', 'question_type']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for question_id, data in self.responses.items():
                    writer.writerow({
                        'question_id': question_id,
                        'question': data['question'],
                        'response': data['response'],
                        'question_type': data['question_type']
                    })
            
            print(f"Responses saved to '{output_file}'")
            return True
            
        except Exception as e:
            print(f"Error saving responses: {e}")
            return False
    
    def analyze_responses(self) -> None:
        """Perform basic analysis on the responses."""
        if not self.responses:
            print("No responses to analyze.")
            return
        
        print(f"\n{'='*50}")
        print("RESPONSE ANALYSIS")
        print(f"{'='*50}")
        
        # Count question types
        type_counts = {}
        yes_no_stats = {"Yes": 0, "No": 0}
        numeric_responses = []
        
        for data in self.responses.values():
            q_type = data['question_type']
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
            
            if q_type == 'yes_no':
                if data['response'] in yes_no_stats:
                    yes_no_stats[data['response']] += 1
            elif q_type == 'number':
                try:
                    numeric_responses.append(float(data['response']))
                except ValueError:
                    pass
        
        print(f"Question Types:")
        for q_type, count in type_counts.items():
            print(f"  {q_type.replace('_', ' ').title()}: {count}")
        
        if yes_no_stats['Yes'] + yes_no_stats['No'] > 0:
            print(f"\nYes/No Responses:")
            total_yn = yes_no_stats['Yes'] + yes_no_stats['No']
            print(f"  Yes: {yes_no_stats['Yes']} ({yes_no_stats['Yes']/total_yn*100:.1f}%)")
            print(f"  No: {yes_no_stats['No']} ({yes_no_stats['No']/total_yn*100:.1f}%)")
        
        if numeric_responses:
            print(f"\nNumeric Response Statistics:")
            print(f"  Count: {len(numeric_responses)}")
            print(f"  Average: {sum(numeric_responses)/len(numeric_responses):.2f}")
            print(f"  Min: {min(numeric_responses)}")
            print(f"  Max: {max(numeric_responses)}")


def main():
    """Main function to run the survey application."""
    app = SurveyApp()
    
    # Get CSV file path from command line argument or user input
    csv_file = None
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        print("Customer Survey Creation Tool MVP")
        print("================================")
        csv_file = input("Enter the path to your CSV file: ").strip()
        if not csv_file:
            print("No file specified. Exiting.")
            return
    
    # Load survey questions
    if not app.load_survey_from_csv(csv_file):
        return
    
    # Conduct the survey
    if app.conduct_survey():
        # Display summary
        app.display_summary()
        
        # Ask if user wants to save responses
        save_choice = input("\nWould you like to save responses to a file? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            app.save_responses()
        
        # Perform analysis
        app.analyze_responses()


if __name__ == "__main__":
    main()