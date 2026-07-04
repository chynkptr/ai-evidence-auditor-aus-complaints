from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "consumer_complaints_2024.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "complaints_clean.csv"
QUALITY_REPORT_PATH = ROOT / "outputs" / "data_quality_report.csv"
MISSING_REPORT_PATH = ROOT / "outputs" / "missing_values_report.csv"

def clean_column_name(name):
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def clean_text(value):
    if pd.isna(value):
        return pd.NA
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value if value else pd.NA

def find_column(columns, keywords):
    for col in columns:
        for keyword in keywords:
            if keyword in col:
                return col
    return None

def main():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

    df_raw = pd.read_csv(RAW_PATH)
    original_rows = len(df_raw)
    original_columns = len(df_raw.columns)

    df = df_raw.copy()
    df.columns = [clean_column_name(col) for col in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(clean_text)

    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)

    date_col = find_column(df.columns, ["date", "received", "created", "lodged"])
    category_col = find_column(df.columns, ["category", "product", "service", "complaint_type", "industry"])
    business_col = find_column(df.columns, ["business", "trader", "supplier", "company", "respondent"])

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        df["complaint_date"] = df[date_col]
        df["complaint_year"] = df["complaint_date"].dt.year
        df["complaint_month"] = df["complaint_date"].dt.to_period("M").astype(str)
        df["complaint_quarter"] = df["complaint_date"].dt.to_period("Q").astype(str)
    else:
        df["complaint_date"] = pd.NaT
        df["complaint_year"] = pd.NA
        df["complaint_month"] = pd.NA
        df["complaint_quarter"] = pd.NA

    if category_col:
        df["category_clean"] = df[category_col].apply(clean_text)
    else:
        df["category_clean"] = pd.NA

    if business_col:
        df["business_clean"] = df[business_col].apply(clean_text)
    else:
        df["business_clean"] = pd.NA

    missing_report = pd.DataFrame({
        "column": df.columns,
        "missing_count": [int(df[col].isna().sum()) for col in df.columns],
        "missing_percent": [round(float(df[col].isna().mean() * 100), 2) for col in df.columns],
        "unique_values": [int(df[col].nunique(dropna=True)) for col in df.columns],
        "dtype": [str(df[col].dtype) for col in df.columns]
    })

    quality_report = pd.DataFrame([
        {"metric": "original_rows", "value": original_rows},
        {"metric": "cleaned_rows", "value": len(df)},
        {"metric": "original_columns", "value": original_columns},
        {"metric": "cleaned_columns", "value": len(df.columns)},
        {"metric": "duplicate_rows_removed", "value": duplicate_rows},
        {"metric": "detected_date_column", "value": date_col or "not_detected"},
        {"metric": "detected_category_column", "value": category_col or "not_detected"},
        {"metric": "detected_business_column", "value": business_col or "not_detected"},
        {"metric": "date_min", "value": str(df["complaint_date"].min()) if df["complaint_date"].notna().any() else "not_available"},
        {"metric": "date_max", "value": str(df["complaint_date"].max()) if df["complaint_date"].notna().any() else "not_available"},
        {"metric": "unique_categories", "value": int(df["category_clean"].nunique(dropna=True))},
        {"metric": "unique_businesses", "value": int(df["business_clean"].nunique(dropna=True))}
    ])

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_PATH, index=False)
    quality_report.to_csv(QUALITY_REPORT_PATH, index=False)
    missing_report.to_csv(MISSING_REPORT_PATH, index=False)

    print("Day 2 cleaning complete")
    print(f"Raw file: {RAW_PATH}")
    print(f"Cleaned file: {PROCESSED_PATH}")
    print(f"Quality report: {QUALITY_REPORT_PATH}")
    print(f"Missing report: {MISSING_REPORT_PATH}")
    print()
    print("Detected columns")
    print(f"Date column: {date_col}")
    print(f"Category column: {category_col}")
    print(f"Business column: {business_col}")
    print()
    print("Cleaned shape")
    print(df.shape)
    print()
    print("Columns")
    print(list(df.columns))

if __name__ == "__main__":
    main()