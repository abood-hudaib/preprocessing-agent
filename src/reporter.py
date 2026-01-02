from __future__ import annotations

import pandas as pd


def generate_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame
) -> str:
    """
    Generate a text report describing preprocessing steps and results.
    """

    report_lines = []

    # Basic shape info
    report_lines.append("DATA PREPROCESSING REPORT")
    report_lines.append("-" * 30)

    report_lines.append(
        f"Rows before cleaning: {original_df.shape[0]}"
    )
    report_lines.append(
        f"Rows after cleaning: {cleaned_df.shape[0]}"
    )
    report_lines.append(
        f"Columns: {original_df.shape[1]}"
    )

    report_lines.append("")

    # Missing values info
    report_lines.append("Missing Values Handling:")
    original_missing = original_df.isnull().sum()
    cleaned_missing = cleaned_df.isnull().sum()

    for col in original_df.columns:
        if original_missing[col] > 0:
            report_lines.append(
                f"- Column '{col}': "
                f"{original_missing[col]} missing values filled"
            )

    report_lines.append("")

    # Duplicate info
    duplicates_removed = (
        original_df.shape[0] - cleaned_df.shape[0]
    )
    report_lines.append(
        f"Duplicate rows removed: {duplicates_removed}"
    )

    report_lines.append("")
    report_lines.append(
        "Preprocessing rules (v1.0):"
    )
    report_lines.append(
        "- Numeric missing values filled with median"
    )
    report_lines.append(
        "- Text missing values filled with 'Unknown'"
    )
    report_lines.append(
        "- Exact duplicate rows removed"
    )

    return "\n".join(report_lines)
