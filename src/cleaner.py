from __future__ import annotations
import yaml
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def load_config(path: str = "config.yml") -> dict:
    """
    Load configuration from YAML file.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def handle_missing_values(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Fill missing values based on config settings.
    """
    cleaned = df.copy()

    # Numeric
    num_strategy = config.get("missing", {}).get("numeric", {}).get("strategy", "median")
    num_fill_val = config.get("missing", {}).get("numeric", {}).get("fill_value", None)

    # Text
    txt_strategy = config.get("missing", {}).get("text", {}).get("strategy", "Unknown")
    txt_fill_val = config.get("missing", {}).get("text", {}).get("fill_value", "Unknown")

    for col in cleaned.columns:
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
                cleaned[col] = cleaned[col].fillna(cleaned[col].mode()[0] if not cleaned[col].mode().empty else txt_fill_val)
            elif txt_strategy == "Unknown":
                cleaned[col] = cleaned[col].fillna("Unknown")
            elif txt_strategy == "constant":
                cleaned[col] = cleaned[col].fillna(txt_fill_val)
            elif txt_strategy == "drop":
                cleaned = cleaned.dropna(subset=[col])

    return cleaned


def handle_duplicates(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Handle duplicates based on config strategy.
    """
    strategy = config.get("duplicates", {}).get("strategy", "remove")

    if strategy == "remove":
        return df.drop_duplicates().copy()
    elif strategy == "keep_first":
        return df.drop_duplicates(keep="first").copy()
    elif strategy == "keep_last":
        return df.drop_duplicates(keep="last").copy()
    elif strategy == "none":
        return df.copy()
    else:
        return df.copy()


def handle_outliers(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Simple outlier handling based on IQR.
    """
    cleaned = df.copy()
    out_cfg = config.get("outliers", {})
    action = out_cfg.get("action", "flag")
    method = out_cfg.get("method", "IQR")

    if method == "IQR":
        for col in cleaned.columns:
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
                # 'flag' does nothing right now, just keep values

    return cleaned


def handle_scaling(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Scale numeric columns based on config.
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

    return cleaned
