from __future__ import annotations


def generate_report(metrics: dict, config: dict, input_file: str) -> str:
    """
    Generate a client-friendly Markdown report.
    """
    missing_cfg = config.get("missing", {})
    num_missing = missing_cfg.get("numeric", {}).get("strategy", "median")
    txt_missing = missing_cfg.get("text", {}).get("strategy", "Unknown")
    dup_strategy = config.get("duplicates", {}).get("strategy", "remove")
    out_cfg = config.get("outliers", {})
    out_action = out_cfg.get("action", "flag")
    out_method = out_cfg.get("method", "IQR")

    lines = []
    lines.append("# Data Preprocessing Report\n")
    lines.append(f"**Input file:** {input_file}\n")

    lines.append("## Summary\n")
    lines.append(f"- Rows before: **{metrics['rows_before']}**")
    lines.append(f"- Rows after: **{metrics['rows_after']}**")
    lines.append(f"- Missing handled (cells reduced): **{metrics['missing_handled']}**")
    lines.append(f"- Duplicates removed (rows): **{metrics['duplicates_removed']}**")
    lines.append(f"- Outliers removed (rows): **{metrics['outliers_removed']}**")
    lines.append(f"- Scaling applied: **{metrics['scaling_applied']}**\n")

    lines.append("## Configuration Used\n")
    lines.append(f"- Missing numeric strategy: **{num_missing}**")
    lines.append(f"- Missing text strategy: **{txt_missing}**")
    lines.append(f"- Duplicates strategy: **{dup_strategy}**")
    lines.append(f"- Outliers: **{out_method}** / action: **{out_action}**\n")

    lines.append("## Delivered Files\n")
    lines.append("- `cleaned_data.csv`")
    lines.append("- `report.md`\n")

    return "\n".join(lines)
