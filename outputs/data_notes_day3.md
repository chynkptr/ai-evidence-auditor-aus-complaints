# Day 3 SQLite and SQL Analysis Notes

## Goal
Load the cleaned consumer complaints dataset into SQLite and create SQL-based business analysis outputs.

## Input file
data/processed/complaints_clean.csv

## Database created
data/processed/complaints.db

## Python script
src/load_to_sqlite.py

## SQL files
- sql/01_schema.sql
- sql/02_business_questions.sql

## SQL analysis completed
- Monthly complaint trend
- Top complaint categories
- Top businesses by complaint count
- Quarterly category trend
- Risk summary by complaint category

## Output files
- outputs/sqlite_table_schema.csv
- outputs/monthly_complaints.csv
- outputs/top_categories.csv
- outputs/top_businesses.csv
- outputs/quarterly_category_trend.csv
- outputs/risk_summary.csv

## Business value
The SQL outputs help identify complaint trends, repeated complaint areas, high-volume businesses, and categories that may need closer review.

## Next step
Day 4 will use these SQL outputs to create an Excel dashboard.