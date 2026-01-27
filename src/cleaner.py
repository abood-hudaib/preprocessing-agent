from __future__ import annotations

from pathlib import Path
import yaml
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def load_config(path: str = "config.yml") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config or {}


def handle_missing_values(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, int]:
    """
    Fill/drop missing values based on config settings.
    Returns: (cleaned_df, missing_handled_count)
    missing_handled_count = total_missing_before - total_missing_after
    """
    cleaned = df.copy()

    missing_cfg = config.get("missing", {})
    num_cfg = missing_cfg.get("numeric", {})
    txt_cfg = missing_cfg.get("text", {})

    num_strategy = num_cfg.get("strategy", "median")
    num_fill_val = num_cfg.get("fill_value", None)

    txt_strategy = txt_cfg.get("strategy", "Unknown")
    txt_fill_val = txt_cfg.get("fill_value", "Unknown")

    missing_before = int(cleaned.isna().sum().sum())

    for col in list(cleaned.columns):
        if pd.api.types.is_numeric_dtype(cleaned[col]):
            if num_strategy == "median":
                cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            elif num_strategy == "mean":
                cleaned[col] = cleaned[col].fillna(cleaned[col].mean())
            elif num_strategy == "zero":
                cleaned[col] = cleaned[col].fillna(0)
            elif num_strategy == "constant" and num_fill_val is not None:
                cleaned[col] = cleaned[col].fillna(num_fill_val)
            elif num_strategy == "drop":
                cleaned = cleaned.dropna(subset=[col])
        else:
            if txt_strategy == "mode":
                mode_vals = cleaned[col].mode()
                fill_value = mode_vals.iloc[0] if not mode_vals.empty else txt_fill_val
                cleaned[col] = cleaned[col].fillna(fill_value)
            elif txt_strategy == "Unknown":
                cleaned[col] = cleaned[col].fillna("Unknown")
            elif txt_strategy == "constant":
                cleaned[col] = cleaned[col].fillna(txt_fill_val)
            elif txt_strategy == "drop":
                cleaned = cleaned.dropna(subset=[col])

    missing_after = int(cleaned.isna().sum().sum())
    missing_handled = max(0, missing_before - missing_after)

    return cleaned, missing_handled


def handle_duplicates(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, int]:
    """
    Handle duplicates based on config strategy.
    Returns: (cleaned_df, duplicates_removed)
    """
    strategy = config.get("duplicates", {}).get("strategy", "remove")

    before = int(df.shape[0])

    if strategy == "remove":
        cleaned = df.drop_duplicates().copy()
    elif strategy == "keep_first":
        cleaned = df.drop_duplicates(keep="first").copy()
    elif strategy == "keep_last":
        cleaned = df.drop_duplicates(keep="last").copy()
    elif strategy == "none":
        cleaned = df.copy()
    else:
        cleaned = df.copy()

    after = int(cleaned.shape[0])
    removed = max(0, before - after)

    return cleaned, removed


def handle_outliers(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, int]:
    """
    Simple outlier handling based on IQR.
    Returns: (cleaned_df, outliers_removed_rows)
    If action != drop => removed = 0
    """
    cleaned = df.copy()
    out_cfg = config.get("outliers", {})
    action = out_cfg.get("action", "flag")
    method = out_cfg.get("method", "IQR")

    before_rows = int(cleaned.shape[0])

    if method == "IQR":
        for col in list(cleaned.columns):
            if pd.api.types.is_numeric_dtype(cleaned[col]):
                Q1 = cleaned[col].quantile(0.25)
                Q3 = cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                if action == "drop":
                    cleaned = cleaned[(cleaned[col] >= lower) & (cleaned[col] <= upper)]
                elif action == "cap":
                    cleaned[col] = cleaned[col].clip(lower, upper)
                # flag => no change

    after_rows = int(cleaned.shape[0])
    removed = max(0, before_rows - after_rows) if action == "drop" else 0

    return cleaned, removed


def handle_scaling(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, str]:
    """
    Scale numeric columns based on config.
    Returns: (cleaned_df, scaling_applied)
    scaling_applied: "standard" | "minmax" | "none"
    """
    cleaned = df.copy()
    method = config.get("scaling", {}).get("numeric", "none")

    num_cols = [col for col in cleaned.columns if pd.api.types.is_numeric_dtype(cleaned[col])]
    scaler = None

    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()

    if scaler is not None and num_cols:
        cleaned[num_cols] = scaler.fit_transform(cleaned[num_cols])
        return cleaned, method

    return cleaned, "none"
