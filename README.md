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

1. Activate the virtual environment (if not already activated)
2. Run the script:
```bash
python keyword_analyzer.py
```

The script will analyze the specified keywords and generate a CSV file with trend data.

## Features

- Analyzes keyword trends over different time periods (3 years, 1 year, 3 months)
- Calculates trend changes and averages
- Exports results to CSV
- Configurable keywords and geographic regions
- Added proper error handling
- Created a class-based structure for better organization
- Added type hints for better code maintainability
- Included progress messages during analysis
- Added support for environment variables (though not required for basic usage)
- Improved code documentation