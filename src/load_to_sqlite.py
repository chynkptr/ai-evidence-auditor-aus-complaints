from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

CLEAN_PATH = ROOT / "data" / "processed" / "complaints_clean.csv"
DB_PATH = ROOT / "data" / "processed" / "complaints.db"
OUTPUTS_DIR = ROOT / "outputs"

QUERY_OUTPUTS = {
    "monthly_complaints": """
        SELECT
            complaint_month,
            COUNT(*) AS total_complaints
        FROM complaints
        WHERE complaint_month IS NOT NULL
        GROUP BY complaint_month
        ORDER BY complaint_month;
    """,
    "top_categories": """
        SELECT
            category_clean,
            COUNT(*) AS total_complaints
        FROM complaints
        WHERE category_clean IS NOT NULL
        GROUP BY category_clean
        ORDER BY total_complaints DESC
        LIMIT 10;
    """,
    "top_businesses": """
        SELECT
            business_clean,
            COUNT(*) AS total_complaints
        FROM complaints
        WHERE business_clean IS NOT NULL
        GROUP BY business_clean
        ORDER BY total_complaints DESC
        LIMIT 10;
    """,
    "quarterly_category_trend": """
        SELECT
            complaint_quarter,
            category_clean,
            COUNT(*) AS total_complaints
        FROM complaints
        WHERE complaint_quarter IS NOT NULL
          AND category_clean IS NOT NULL
        GROUP BY complaint_quarter, category_clean
        ORDER BY complaint_quarter, total_complaints DESC;
    """,
    "risk_summary": """
        WITH category_counts AS (
            SELECT
                category_clean,
                COUNT(*) AS total_complaints,
                COUNT(DISTINCT business_clean) AS unique_businesses
            FROM complaints
            WHERE category_clean IS NOT NULL
            GROUP BY category_clean
        ),
        recent_counts AS (
            SELECT
                category_clean,
                COUNT(*) AS recent_complaints
            FROM complaints
            WHERE category_clean IS NOT NULL
              AND complaint_month IN (
                  SELECT complaint_month
                  FROM complaints
                  WHERE complaint_month IS NOT NULL
                  GROUP BY complaint_month
                  ORDER BY complaint_month DESC
                  LIMIT 3
              )
            GROUP BY category_clean
        )
        SELECT
            c.category_clean,
            c.total_complaints,
            c.unique_businesses,
            COALESCE(r.recent_complaints, 0) AS recent_complaints,
            ROUND(
                c.total_complaints * 0.6 +
                COALESCE(r.recent_complaints, 0) * 0.3 +
                c.unique_businesses * 0.1,
                2
            ) AS risk_score
        FROM category_counts c
        LEFT JOIN recent_counts r
            ON c.category_clean = r.category_clean
        ORDER BY risk_score DESC
        LIMIT 15;
    """
}

def main():
    if not CLEAN_PATH.exists():
        raise FileNotFoundError(f"Cleaned file not found: {CLEAN_PATH}")

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CLEAN_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("complaints", conn, if_exists="replace", index=False)

        table_info = pd.read_sql_query("PRAGMA table_info(complaints);", conn)
        table_info.to_csv(OUTPUTS_DIR / "sqlite_table_schema.csv", index=False)

        for name, query in QUERY_OUTPUTS.items():
            result = pd.read_sql_query(query, conn)
            result.to_csv(OUTPUTS_DIR / f"{name}.csv", index=False)

    print("Day 3 SQLite and SQL analysis complete")
    print(f"Database created: {DB_PATH}")
    print("SQL outputs created:")
    for name in QUERY_OUTPUTS:
        print(f"- outputs/{name}.csv")
    print("- outputs/sqlite_table_schema.csv")

if __name__ == "__main__":
    main()