from __future__ import annotations

import argparse
from pathlib import Path

from src.loader import load_data
from src.cleaner import (
    load_config,
    handle_missing_values,
    handle_duplicates,
    handle_outliers,
    handle_scaling,
)
from src.reporter import generate_report

from src.type_validator import infer_column_types, print_type_validation_report
from src.missing_strategy import recommend_missing_strategies, print_missing_strategy_report
from src.profiler import extended_profile, print_profile_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data Preprocessing Agent")
    parser.add_argument("--input", required=True, help="Path to input dataset (CSV/TXT or Excel).")
    parser.add_argument("--config", default="config.yml", help="Path to config.yml (default: config.yml).")
    parser.add_argument("--output", default="outputs", help="Output folder (default: outputs).")

    # Client file robustness
    parser.add_argument("--sep", default=None, help="CSV separator, e.g. ',' or ';' (optional).")
    parser.add_argument("--encoding", default=None, help="CSV encoding, e.g. utf-8-sig, cp1256 (optional).")

    # Output format
    parser.add_argument(
        "--out-format",
        choices=["csv", "xlsx"],
        default="csv",
        help="Output format for cleaned data (default: csv).",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    config_path = Path(args.config)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load (robust)
    df = load_data(str(input_path), encoding=args.encoding, sep=args.sep)
    config = load_config(str(config_path))

    # Optional console insights (helpful for you)
    type_report = infer_column_types(df)
    print_type_validation_report(type_report)

    profile_before = extended_profile(df)
    print_profile_report(profile_before)

    strategy_report = recommend_missing_strategies(df, type_report)
    print_missing_strategy_report(strategy_report)

    # Preprocessing with metrics
    rows_before = int(df.shape[0])

    df_clean, missing_handled = handle_missing_values(df, config)
    df_clean, duplicates_removed = handle_duplicates(df_clean, config)
    df_clean, outliers_removed = handle_outliers(df_clean, config)
    df_clean, scaling_applied = handle_scaling(df_clean, config)

    rows_after = int(df_clean.shape[0])

    # Save cleaned data
    if args.out_format == "xlsx":
        cleaned_path = output_dir / "cleaned_data.xlsx"
        df_clean.to_excel(cleaned_path, index=False)
    else:
        cleaned_path = output_dir / "cleaned_data.csv"
        df_clean.to_csv(cleaned_path, index=False)

    # Generate report
    metrics = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "missing_handled": int(missing_handled),
        "duplicates_removed": int(duplicates_removed),
        "outliers_removed": int(outliers_removed),
        "scaling_applied": str(scaling_applied),
    }

    report_text = generate_report(metrics, config, str(input_path))
    report_path = output_dir / "report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print("=== Preprocessing Completed ===")
    print(f"Cleaned data saved to: {cleaned_path}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
