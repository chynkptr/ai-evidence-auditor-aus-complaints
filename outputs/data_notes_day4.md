# Day 4 Excel Dashboard Notes

## Goal
Create an Excel dashboard using SQL outputs from the cleaned Australian consumer complaints dataset.

## Input files
- outputs/monthly_complaints.csv
- outputs/top_categories.csv
- outputs/top_businesses.csv
- outputs/quarterly_category_trend.csv
- outputs/risk_summary.csv

## Python script
src/export_excel.py

## Excel output
outputs/complaints_dashboard.xlsx

## Workbook sheets
- Dashboard
- Monthly Trend
- Top Categories
- Top Businesses
- Quarterly Trend
- Risk Summary

## Dashboard contents
- Total complaints
- Top complaint category
- Top business by complaint count
- Highest risk category
- Monthly complaint trend chart
- Top complaint categories chart
- Top businesses chart
- Highest risk categories chart
- Analyst notes

## Business value
The dashboard gives a quick view of complaint trends, repeated complaint areas, and categories that may require closer review.

## Next step
Day 5 will add a GenAI executive summary layer that validates AI-generated findings against SQL outputs.