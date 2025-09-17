# Customer Survey Creation Tool MVP

A console-based Python application that creates interactive surveys from CSV files and captures user responses for analysis.

## Features

- **CSV-Based Survey Creation**: Load survey questions from structured CSV files
- **Interactive Console Interface**: User-friendly command-line survey experience
- **Multiple Question Types**: Support for text, number, multiple choice, and yes/no questions
- **Input Validation**: Robust validation for all question types
- **Response Analysis**: Basic statistical analysis of survey responses
- **Data Export**: Save responses to CSV files for further analysis
- **Real-time Summary**: Display survey summary upon completion

## Installation

No external dependencies required! This application uses only Python standard library modules.

```bash
# Clone the repository
git clone https://github.com/IoanaLivia/Padawan-Integration-Hackathon-Day-1.git
cd Padawan-Integration-Hackathon-Day-1

# Run the application (requires Python 3.6+)
python3 survey_app.py sample_survey.csv
```

## Usage

### Running a Survey

```bash
# With command line argument
python3 survey_app.py your_survey.csv

# Interactive mode (prompts for file path)
python3 survey_app.py
```

### CSV File Format

Create a CSV file with the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| question_id | Unique identifier for the question | Yes |
| question_text | The question to display to users | Yes |
| question_type | Type of question (see below) | Yes |
| options | Comma-separated options for multiple_choice questions | No |

### Supported Question Types

1. **text**: Free-form text input
2. **number**: Numeric input (integers or decimals)
3. **multiple_choice**: Choose from predefined options
4. **yes_no**: Yes/No questions

### Example CSV Format

```csv
question_id,question_text,question_type,options
q1,What is your name?,text,
q2,How old are you?,number,
q3,What is your favorite color?,multiple_choice,"Red,Blue,Green,Yellow,Purple"
q4,Do you enjoy programming?,yes_no,
q5,Any comments?,text,
```

**Important**: For multiple choice questions, wrap options in quotes to handle comma-separated values correctly.

## Sample Survey

The repository includes `sample_survey.csv` with example questions demonstrating all question types:

- Text input (name, comments)
- Numeric input (age, experience years)
- Multiple choice (favorite color, programming language)
- Yes/No questions (satisfaction, preferences)

## Output

The application provides:

1. **Interactive Survey Experience**: Step-by-step question presentation with validation
2. **Survey Summary**: Complete overview of all responses
3. **Response Export**: CSV file with timestamp for data persistence
4. **Statistical Analysis**: 
   - Question type distribution
   - Yes/No response percentages
   - Numeric response statistics (count, average, min, max)

## Example Output

```
==================================================
Welcome to the Sample Survey Survey!
==================================================

Question 1 of 8
------------------------------
What is your name?
Enter your response:
> John Smith

[... interactive survey continues ...]

==================================================
RESPONSE ANALYSIS
==================================================
Question Types:
  Text: 2
  Number: 2
  Multiple Choice: 2
  Yes No: 2

Yes/No Responses:
  Yes: 2 (100.0%)
  No: 0 (0.0%)

Numeric Response Statistics:
  Count: 2
  Average: 17.50
  Min: 5.0
  Max: 30.0
```

## Features for Business Use

- **Data Collection**: Efficiently gather structured feedback from users
- **Quality Assurance**: Built-in validation ensures data integrity
- **Analysis Ready**: Responses exported in CSV format for further analysis
- **User Experience**: Intuitive interface reduces survey abandonment
- **Scalable**: Easy to create new surveys by modifying CSV files

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses standard library only)
- **File Encoding**: UTF-8
- **Error Handling**: Comprehensive validation and error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Work Item Reference

**AB#22820** - Customer Survey Creation Tool MVP implementation

This MVP fulfills the requirements for a complex Customer Survey Creation Tool that:
- ✅ Takes CSV files as input
- ✅ Creates console-based survey applications
- ✅ Captures and validates user responses
- ✅ Processes responses for analysis
- ✅ Provides comprehensive error handling
- ✅ Includes documentation and examples