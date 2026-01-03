from __future__ import annotations
import pandas as pd


def basic_profile(df: pd.DataFrame) -> dict:
    """
    A basic data profile summary.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "types": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "unique_counts": df.nunique().to_dict(),
    }


def extended_profile(df: pd.DataFrame) -> dict:
    """
    Extended profile including simple stats and top values.
    """
    profile = basic_profile(df)
    extended = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe().to_dict()

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            extended[col] = {
                "numeric_stats": desc,
                "iqr_outlier_bounds": (
                    float(Q1 - 1.5 * IQR),
                    float(Q3 + 1.5 * IQR),
                ),
            }
        else:
            top = df[col].value_counts(normalize=True).head(3)
            extended[col] = {
                "top_values": top.to_dict()
            }

    profile["extended"] = extended
    return profile


def print_profile_report(profile: dict) -> None:
    """
    Print a nicely formatted profiling report in English.
    """

    print("\n=== Data Profiling Report ===\n")
    print(f"• Total rows: {profile['rows']}")
    print(f"• Total columns: {profile['columns']}\n")

    # Missing values
    print("📌 Missing Values:")
    found_missing = False
    for col, count in profile["missing"].items():
        if count > 0:
            print(f"  - {col}: {count} missing")
            found_missing = True
    if not found_missing:
        print("  None found.")
    print()

    # Unique counts
    print("🔢 Unique Values Count:")
    for col, cnt in profile["unique_counts"].items():
        print(f"  - {col}: {cnt}")
    print()

    # Types
    print("📊 Data Types:")
    for col, dtype in profile["types"].items():
        print(f"  - {col}: {dtype}")
    print()

    # Numeric column stats
    print("📈 Numeric Column Statistics:")
    for col, details in profile["extended"].items():
        if "numeric_stats" in details:
            stats = details["numeric_stats"]
            print(f"  - {col}: mean={stats.get('mean')}, median={stats.get('50%')}, min={stats.get('min')}, max={stats.get('max')}")
    print()

    # Top values for text columns
    print("🏷️ Top Categories for Text Columns:")
    for col, details in profile["extended"].items():
        if "top_values" in details:
            print(f"  - {col}:")
            for value, pct in details["top_values"].items():
                seen_pct = round(pct * 100, 2)
                print(f"      {value} — {seen_pct}%")
    print()
