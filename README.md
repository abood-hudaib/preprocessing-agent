# Data Preprocessing Agent (v1.0)

A simple and robust data preprocessing agent built using Python and pandas.

## What this project does
- Loads CSV datasets
- Fills missing values:
  - Numeric columns → median
  - Text columns → "Unknown"
- Removes duplicate rows
- Generates a clear preprocessing report

## Project Structure
preprocessing_agent/
- main.py
- data.csv
- README.md
- src/
  - loader.py
  - cleaner.py
  - reporter.py

## How to run
pip install pandas  
python main.py

## Version
v1.0 — Clean & Report
