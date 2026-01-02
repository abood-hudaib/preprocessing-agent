from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from a CSV or Excel file and return it as a DataFrame.
    v1.0 supports: .csv, .xlsx, .xls
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    elif suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use CSV or Excel.")
