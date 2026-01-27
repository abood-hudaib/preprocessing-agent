from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_data(file_path: str, *, encoding: str | None = None, sep: str | None = None) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()

    if ext in [".csv", ".txt"]:
        # If user provided encoding, try it first
        encodings_to_try = [encoding] if encoding else []
        # common encodings for clients (including Arabic Windows encoding)
        encodings_to_try += ["utf-8", "utf-8-sig", "cp1256", "cp1252"]

        last_error: Exception | None = None
        for enc in encodings_to_try:
            try:
                return pd.read_csv(path, encoding=enc, sep=sep if sep else ",")
            except Exception as e:
                last_error = e

        raise ValueError(
            "Failed to read CSV. Try providing --encoding and/or --sep. "
            f"Last error: {last_error}"
        )

    if ext in [".xlsx", ".xls"]:
        try:
            return pd.read_excel(path)
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

    raise ValueError("Unsupported file format. Please use CSV or Excel.")
