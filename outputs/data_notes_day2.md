# Day 2 Data Cleaning Notes

## Goal
Clean the raw Australian consumer complaints dataset and create analysis-ready outputs.

## Input file
data/raw/consumer_complaints_2024.csv

## Python script
src/clean_data.py

## Cleaning steps completed
- Standardised column names
- Removed duplicate rows
- Cleaned text spacing
- Parsed complaint date column where available
- Created complaint year, month, and quarter fields
- Created cleaned category and business fields
- Exported cleaned dataset
- Exported data quality report
- Exported missing values report

## Output files
- data/processed/complaints_clean.csv
- outputs/data_quality_report.csv
- outputs/missing_values_report.csv

## Checks completed
- Confirmed raw dataset loaded successfully
- Confirmed cleaned dataset was exported
- Confirmed data quality report was created
- Confirmed missing values report was created

## Notes
The cleaned dataset will be used in Day 3 for SQLite loading and SQL-based business analysis.