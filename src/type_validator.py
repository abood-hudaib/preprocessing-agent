import pandas as pd


def infer_column_types(df: pd.DataFrame) -> dict:
    """
    Infer and validate column types.
    Returns a structured report dictionary.
    """
    report = {}

    total_rows = len(df)

    for col in df.columns:
        series = df[col]
        col_report = {}

        # Missing values
        missing_count = series.isna().sum()
        missing_ratio = missing_count / total_rows if total_rows > 0 else 0

        # Try numeric conversion
        numeric_converted = pd.to_numeric(series, errors="coerce")
        numeric_valid = numeric_converted.notna().sum()
        numeric_ratio = numeric_valid / total_rows if total_rows > 0 else 0

        # Try datetime conversion
        datetime_converted = pd.to_datetime(series, errors="coerce")
        datetime_valid = datetime_converted.notna().sum()
        datetime_ratio = datetime_valid / total_rows if total_rows > 0 else 0

        # Uniqueness
        unique_count = series.nunique(dropna=True)
        uniqueness_ratio = unique_count / total_rows if total_rows > 0 else 0

        # Decide detected type
        detected_type = "text"
        suggestion = "keep as text"
        notes = []

        if numeric_ratio > 0.7:
            detected_type = "numeric"
            suggestion = "convert to numeric"
        elif datetime_ratio > 0.6:
            detected_type = "datetime"
            suggestion = "parse as datetime"

        if uniqueness_ratio > 0.95:
            notes.append("Likely identifier (high uniqueness)")

        if numeric_ratio > 0.3 and numeric_ratio < 0.7:
            notes.append("Mixed numeric/text values")

        col_report["detected_type"] = detected_type
        col_report["numeric_parsable_%"] = round(numeric_ratio * 100, 2)
        col_report["datetime_parsable_%"] = round(datetime_ratio * 100, 2)
        col_report["missing_%"] = round(missing_ratio * 100, 2)
        col_report["uniqueness_%"] = round(uniqueness_ratio * 100, 2)
        col_report["suggested_action"] = suggestion
        col_report["notes"] = notes

        report[col] = col_report

    return report


def print_type_validation_report(type_report: dict) -> None:
    """
    Print a human-readable column type validation report.
    """
    print("\n=== Column Type Validation Report ===\n")

    for col, info in type_report.items():
        print(f"Column: {col}")
        print("-" * (8 + len(col)))
        print(f"Detected type: {info['detected_type']}")
        print(f"Numeric parsable: {info['numeric_parsable_%']}%")
        print(f"Datetime parsable: {info['datetime_parsable_%']}%")
        print(f"Missing values: {info['missing_%']}%")
        print(f"Uniqueness: {info['uniqueness_%']}%")
        print(f"Suggested action: {info['suggested_action']}")

        if info["notes"]:
            print("Notes:")
            for note in info["notes"]:
                print(f" - {note}")

        print()
