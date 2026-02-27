"""
Level 1 - Job Example
=====================
This script runs as a CML Job task.

It demonstrates:
  - Reading environment variables passed from .project-metadata.yaml
  - Using pandas to generate a simple data report
  - Writing output to a file (persisted in the project filesystem)
  - Structured logging suitable for CML Job history logs
"""

import os
import json
import platform
import sys
from datetime import datetime

import pandas as pd


REPORT_DIR = os.environ.get("REPORT_OUTPUT_DIR", "outputs")
REPORT_NAME = os.environ.get("REPORT_NAME", "data_report")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def create_sample_dataset() -> pd.DataFrame:
    """Create a small in-memory dataset to simulate a real data pipeline."""
    data = {
        "product":    ["Cloudera AI", "CML Sessions", "CML Jobs", "CML Models", "CML Apps"],
        "category":   ["Platform",    "Compute",      "Compute",  "Serving",    "Serving"],
        "usage_score": [98,            87,              76,         91,           83],
        "active_users":[500,           320,             210,        180,          145],
    }
    return pd.DataFrame(data)


def generate_summary(df: pd.DataFrame) -> dict:
    """Compute descriptive statistics and group summaries."""
    summary = {
        "generated_at": datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "usage_score": {
            "mean":  round(df["usage_score"].mean(), 2),
            "max":   int(df["usage_score"].max()),
            "min":   int(df["usage_score"].min()),
            "top_product": df.loc[df["usage_score"].idxmax(), "product"],
        },
        "active_users": {
            "total": int(df["active_users"].sum()),
            "mean":  round(df["active_users"].mean(), 2),
        },
        "by_category": (
            df.groupby("category")["active_users"]
            .sum()
            .rename("total_users")
            .reset_index()
            .to_dict(orient="records")
        ),
    }
    return summary


def save_outputs(df: pd.DataFrame, summary: dict):
    """Persist CSV and JSON report to the output directory."""
    os.makedirs(REPORT_DIR, exist_ok=True)

    csv_path  = os.path.join(REPORT_DIR, f"{REPORT_NAME}.csv")
    json_path = os.path.join(REPORT_DIR, f"{REPORT_NAME}.json")

    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    log(f"CSV  saved → {csv_path}")
    log(f"JSON saved → {json_path}")
    return csv_path, json_path


def print_report(summary: dict):
    """Print a human-readable summary to the Job log."""
    print()
    print("=" * 55)
    print("  DATA REPORT SUMMARY")
    print("=" * 55)
    print(f"  Generated at  : {summary['generated_at']}")
    print(f"  Rows / Columns: {summary['row_count']} / {summary['column_count']}")
    print()
    print("  [Usage Score]")
    print(f"    Mean        : {summary['usage_score']['mean']}")
    print(f"    Max         : {summary['usage_score']['max']}")
    print(f"    Min         : {summary['usage_score']['min']}")
    print(f"    Top Product : {summary['usage_score']['top_product']}")
    print()
    print("  [Active Users]")
    print(f"    Total       : {summary['active_users']['total']}")
    print(f"    Mean        : {summary['active_users']['mean']}")
    print()
    print("  [By Category]")
    for row in summary["by_category"]:
        print(f"    {row['category']:<12}: {row['total_users']} users")
    print("=" * 55)
    print()


def main():
    log("Job started")
    log(f"Output directory : {REPORT_DIR}")
    log(f"Report name      : {REPORT_NAME}")
    print()

    log("Creating sample dataset...")
    df = create_sample_dataset()

    log("Generating summary statistics...")
    summary = generate_summary(df)

    log("Saving outputs...")
    save_outputs(df, summary)

    print_report(summary)

    log("Job completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
