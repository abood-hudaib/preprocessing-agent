import pandas as pd

def recommend_missing_strategies(df: pd.DataFrame, type_report: dict) -> dict:
    """
    Generate recommended missing value strategies for each column,
    based on type inference and missing ratios.
    """
    recommendations = {}

    for col in df.columns:
        info = type_report.get(col, {})
        missing_pct = info.get("missing_%", 0)
        detected = info.get("detected_type", "text")

        rec = {"column": col, "detected_type": detected, "missing_%": missing_pct}

        # Numeric columns
        if detected == "numeric":
            if missing_pct == 0:
                rec["suggestion"] = "No missing"
            elif missing_pct < 5:
                rec["suggestion"] = "median"
                rec["reason"] = "Low missing ratio, median is robust"   
            elif missing_pct < 20:
                rec["suggestion"] = "median + flag"
                rec["reason"] = (
                    "Moderate missing ratio; median plus indicator is helpful"
                )
            else:
                rec["suggestion"] = "median OR drop column"
                rec["reason"] = (
                    "High missing ratio; may consider dropping if not essential"
                )

        # Text columns
        elif detected == "text":
            if missing_pct == 0:
                rec["suggestion"] = "No missing"
            elif missing_pct < 10:
                rec["suggestion"] = "mode"
                rec["reason"] = "Low text missing; fill with most frequent"
            elif missing_pct < 30:
                rec["suggestion"] = "Unknown"
                rec["reason"] = "Moderate missing; assign 'Unknown'"
            else:
                rec["suggestion"] = "drop OR Unknown"
                rec["reason"] = (
                    "High missing ratio; consider dropping column if not useful"
                )

        # Datetime or others
        else:
            if missing_pct == 0:
                rec["suggestion"] = "No missing"
            elif missing_pct < 15:
                rec["suggestion"] = "fill with mode or custom datetime"
                rec["reason"] = "Low missing in datetime-like, careful parsing"
            else:
                rec["suggestion"] = "Investigate or drop"
                rec["reason"] = (
                    "High missing ratio for datetime; manual review recommended"
                )

        recommendations[col] = rec

    return recommendations


def print_missing_strategy_report(strategy_report: dict) -> None:
    """
    Print a human-readable missing strategy recommendation report.
    """
    print("\n=== Missing Value Strategy Recommendation ===\n")

    for col, info in strategy_report.items():
        print(f"Column: {col}")
        print("-" * (8 + len(col)))
        print(f"Detected type: {info['detected_type']}")
        print(f"Missing percentage: {info['missing_%']}%")
        print(f"Suggested strategy: {info['suggestion']}")

        reason = info.get("reason")
        if reason:
            print(f"Reason: {reason}")

        print()
