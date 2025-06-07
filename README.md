# Keyword Trend Analyzer

A Python tool that analyzes keyword trends using the Google Trends API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your keywords in a CSV file (default: `keywords.csv`):
   - The file must contain a 'Keyword' column
   - Example:
     ```csv
     Keyword
     conversation starters for dating
     emotional regulation app
     conflict resolution in relationships
     ```

2. Run the script:
```bash
python keyword_analyzer.py
```

### Command Line Options

- `--input` or `-i`: Specify input CSV file (default: keywords.csv)
- `--output` or `-o`: Specify output CSV file (default: keyword_trends_comparison.csv)
- `--geo` or `-g`: Specify geographic region (default: US)

Example:
```bash
python keyword_analyzer.py --input my_keywords.csv --output results.csv --geo UK
```

## Features

- Analyzes keyword trends over different time periods (1 year, 3 months, 1 month)
- Calculates trend changes and averages
- Configurable geographic regions
- Exports results to CSV
- Added proper error handling
- Created a class-based structure for better organization
- Added type hints for better code maintainability
- Included progress messages during analysis
- Added support for environment variables (though not required for basic usage)
- Improved code documentation