SELECT
    complaint_month,
    COUNT(*) AS total_complaints
FROM complaints
WHERE complaint_month IS NOT NULL
GROUP BY complaint_month
ORDER BY complaint_month;

SELECT
    category_clean,
    COUNT(*) AS total_complaints
FROM complaints
WHERE category_clean IS NOT NULL
GROUP BY category_clean
ORDER BY total_complaints DESC
LIMIT 10;

SELECT
    business_clean,
    COUNT(*) AS total_complaints
FROM complaints
WHERE business_clean IS NOT NULL
GROUP BY business_clean
ORDER BY total_complaints DESC
LIMIT 10;

SELECT
    complaint_quarter,
    category_clean,
    COUNT(*) AS total_complaints
FROM complaints
WHERE complaint_quarter IS NOT NULL
  AND category_clean IS NOT NULL
GROUP BY complaint_quarter, category_clean
ORDER BY complaint_quarter, total_complaints DESC;

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