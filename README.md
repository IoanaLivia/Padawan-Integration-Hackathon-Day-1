# Customer Survey Creation Tool MVP

A comprehensive Python-based console application that creates interactive surveys from CSV files, collects user responses, and provides analysis of the collected data.

## Features

- **CSV-driven survey creation**: Load survey questions from CSV files with support for multiple question types
- **Interactive console interface**: User-friendly command-line survey experience
- **Multiple question types**:
  - Text input questions
  - Multiple choice questions (with numbered or text selection)
  - Rating questions (1-10 scale)
  - Yes/No questions
- **Response validation**: Ensures data quality with built-in validation for each question type
- **Data persistence**: Automatically saves responses to JSON files with timestamps
- **Real-time analysis**: Provides statistical analysis of collected responses
- **Error handling**: Robust error handling for malformed CSV files and invalid responses
- **Sample data generation**: Built-in sample CSV creator for quick testing

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## CSV File Format

The CSV file should contain the following columns:

| Column | Description | Required | Examples |
|--------|-------------|----------|----------|
| question_id | Unique identifier for the question | Yes | q1, question_001, satisfaction |
| question_text | The actual question to display | Yes | "What is your overall satisfaction?" |
| question_type | Type of question | Yes | text, multiple_choice, rating, yes_no |
| options | Available options (for multiple_choice) | No | "Excellent\|Good\|Fair\|Poor" |
| required | Whether the question is required | No | true, false (default: true) |

### Question Types

1. **text**: Free-form text input
2. **multiple_choice**: Select from predefined options (separated by `|`)
3. **rating**: Numeric rating from 1-10
4. **yes_no**: Simple yes/no questions

### Sample CSV Content

```csv
question_id,question_text,question_type,options,required
q1,What is your overall satisfaction with our service?,rating,,true
q2,Which of the following best describes your experience?,multiple_choice,"Excellent|Good|Fair|Poor",true
q3,Would you recommend our service to others?,yes_no,,true
q4,Please provide any additional comments:,text,,false
```

## Usage

### Running a Survey

```bash
python survey_tool.py <csv_file>
```

Example:
```bash
python survey_tool.py sample_survey.csv
```

### Creating a Sample CSV

```bash
python survey_tool.py --create-sample
```

This will create a `sample_survey.csv` file with example questions that you can use for testing.

### Survey Flow

1. Load questions from the specified CSV file
2. Display welcome message and instructions
3. Present questions one by one with appropriate input prompts
4. Validate responses based on question type
5. Save all responses to a timestamped JSON file
6. Display analysis of collected responses

### User Experience

- Users can type 'quit' at any time to exit the survey
- Required questions must be answered before proceeding
- Multiple choice questions accept both number selections and text matches
- Rating questions only accept numbers 1-10
- Clear error messages guide users when invalid responses are entered

## Output Files

### Response Data
Responses are automatically saved to JSON files named `survey_responses_YYYYMMDD_HHMMSS.json` containing:

```json
[
  {
    "q1": "8",
    "q2": "Good",
    "q3": "yes",
    "q4": "Great service overall!",
    "timestamp": "2024-01-15T10:30:45.123456",
    "completed": true
  }
]
```

### Analysis Output
The tool provides immediate analysis including:
- Total number of responses
- Average ratings for numeric questions
- Response distribution for multiple choice questions
- All responses for text questions

## Error Handling

- **File not found**: Clear error message when CSV file doesn't exist
- **Malformed CSV**: Warnings for rows with missing required fields
- **Invalid responses**: User-friendly prompts to correct invalid input
- **Empty surveys**: Graceful handling when no valid questions are loaded

## Project Structure

```
├── survey_tool.py          # Main application file
├── sample_survey.csv       # Sample CSV file (generated)
├── survey_responses_*.json # Response data files (generated)
└── README.md              # This documentation
```

## Development Notes

This MVP was created as part of AB#22820 and includes:
- Clean, modular Python code with proper error handling
- Comprehensive documentation and examples
- Extensible design for future enhancements
- No external dependencies for easy deployment

## Future Enhancements

Potential improvements could include:
- Web-based interface
- Database integration
- Advanced analytics and visualization
- Multi-language support
- Question branching and conditional logic
- Export to various formats (PDF, Excel, etc.)