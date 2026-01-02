from __future__ import annotations

import pandas as pd


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in a DataFrame (v1.0 rules):
    - Numeric columns: fill NaN with median
    - Non-numeric columns: fill NaN with "Unknown"
    Note: Date handling is intentionally excluded in v1.0.
    """
    cleaned = df.copy()

    for col in cleaned.columns:
        if pd.api.types.is_numeric_dtype(cleaned[col]):
            median_value = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(median_value)
        else:
            cleaned[col] = cleaned[col].fillna("Unknown")

    return cleaned


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows (exact duplicates).
    """
    return df.drop_duplicates().copy()
