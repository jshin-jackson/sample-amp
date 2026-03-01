"""
Level 5 - Model API Integration
=================================
This script runs as a CML Application (start_application task).

It demonstrates:
  - Required environment variable validation (DASHBOARD_TITLE)
  - Optional env vars that change runtime behavior (SCORE_ALERT_THRESHOLD,
    ENABLE_RAW_DATA_DOWNLOAD)
  - Type conversion for env var values (str → int, str → bool)
  - Graceful error messaging when required config is missing
  - Live REST API call to a deployed CML Model for real-time predictions
    (MODEL_ENDPOINT_URL, MODEL_API_KEY)
"""

import os
import json
from pathlib import Path

import requests
import pandas as pd
import streamlit as st


# ── Environment Variables ──────────────────────────────────────────────────────
# Level 2: file I/O config
REPORT_DIR  = os.environ.get("REPORT_OUTPUT_DIR", "outputs")
REPORT_NAME = os.environ.get("REPORT_NAME", "data_report")

# Level 3: runtime behavior config
DASHBOARD_TITLE          = os.environ.get("DASHBOARD_TITLE", "")
SCORE_ALERT_THRESHOLD    = int(os.environ.get("SCORE_ALERT_THRESHOLD", "80"))
ENABLE_RAW_DATA_DOWNLOAD = os.environ.get("ENABLE_RAW_DATA_DOWNLOAD", "true").lower() == "true"

# Level 5: model API config
MODEL_ENDPOINT_URL = os.environ.get("MODEL_ENDPOINT_URL", "")
MODEL_API_KEY      = os.environ.get("MODEL_API_KEY", "")

CSV_PATH  = Path(REPORT_DIR) / f"{REPORT_NAME}.csv"
JSON_PATH = Path(REPORT_DIR) / f"{REPORT_NAME}.json"


st.set_page_config(
    page_title="Hello World AMP Dashboard",
    page_icon="🌐",
    layout="wide",
)


# ── Model API Helper ───────────────────────────────────────────────────────────

def call_model(active_users: int) -> dict:
    """Call the deployed Usage Score Predictor REST API."""
    payload = {"request": {"active_users": active_users}}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MODEL_API_KEY}",
    }
    resp = requests.post(MODEL_ENDPOINT_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ── Validate Required Environment Variables ────────────────────────────────────

if not DASHBOARD_TITLE:
    st.error(
        "**Required environment variable `DASHBOARD_TITLE` is not set.**\n\n"
        "This variable is required to run the dashboard. Please set it before deploying:\n\n"
        "1. Go to **AMPs** → redeploy and set `DASHBOARD_TITLE` in the Environment Variables step, or\n"
        "2. Go to **Applications** → Edit this application and add the environment variable.\n\n"
        "Example value: `My Team's Data Report Dashboard`",
        icon="🚫",
    )
    st.stop()


# ── Header ────────────────────────────────────────────────────────────────────

st.title(DASHBOARD_TITLE)
st.caption(
    f"Level 5 · Cloudera AI · Applied ML Prototype · "
    f"Alert threshold: **{SCORE_ALERT_THRESHOLD}** · "
    f"Downloads: **{'enabled' if ENABLE_RAW_DATA_DOWNLOAD else 'disabled'}**"
)
st.divider()


# ── Check if Job has been run ─────────────────────────────────────────────────

if not CSV_PATH.exists() or not JSON_PATH.exists():
    st.warning(
        f"Report files not found in `{REPORT_DIR}/`. "
        "Please run the **Data Report Job** first from the Jobs menu, "
        "then refresh this page.",
        icon="⚠️",
    )
    st.info(
        "**How to run the Job:**\n"
        "1. Go to **Jobs** in the left menu\n"
        "2. Click **Data Report Job**\n"
        "3. Click **Run Job**\n"
        "4. Come back here and refresh",
        icon="ℹ️",
    )
    st.stop()


# ── Load data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    with open(JSON_PATH) as f:
        summary = json.load(f)
    return df, summary


df, summary = load_data()


# ── KPI Metrics ───────────────────────────────────────────────────────────────

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Active Users",
    value=f"{summary['active_users']['total']:,}",
)
col2.metric(
    label="Avg Usage Score",
    value=summary["usage_score"]["mean"],
)
col3.metric(
    label="Top Product",
    value=summary["usage_score"]["top_product"],
)
col4.metric(
    label="Products Tracked",
    value=summary["row_count"],
)

st.divider()


# ── High Performers (Level 3) ─────────────────────────────────────────────────

high_performers = df[df["usage_score"] >= SCORE_ALERT_THRESHOLD].copy()

if not high_performers.empty:
    st.subheader(f"🏆 High Performers  (score ≥ {SCORE_ALERT_THRESHOLD})")
    hp_cols = st.columns(len(high_performers))
    for col, (_, row) in zip(hp_cols, high_performers.iterrows()):
        col.metric(
            label=row["product"],
            value=int(row["usage_score"]),
            delta=f"+{int(row['usage_score']) - SCORE_ALERT_THRESHOLD} above threshold",
        )
    st.divider()


# ── Charts ────────────────────────────────────────────────────────────────────

chart_col, table_col = st.columns([3, 2])

with chart_col:
    st.subheader("Usage Score by Product")
    chart_df = df.set_index("product")[["usage_score"]]
    st.bar_chart(chart_df, color="#00BC73", height=300)

with table_col:
    st.subheader("Active Users by Category")
    category_data = pd.DataFrame(summary["by_category"])
    category_data.columns = ["Category", "Total Users"]
    st.dataframe(
        category_data,
        use_container_width=True,
        hide_index=True,
    )

st.divider()


# ── Raw Data Table ────────────────────────────────────────────────────────────

with st.expander("Raw Dataset", expanded=False):
    display_df = df.copy()
    display_df["★"] = display_df["usage_score"].apply(
        lambda s: "🏆" if s >= SCORE_ALERT_THRESHOLD else ""
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if ENABLE_RAW_DATA_DOWNLOAD:
        st.download_button(
            label="Download CSV",
            data=CSV_PATH.read_bytes(),
            file_name=CSV_PATH.name,
            mime="text/csv",
        )
    else:
        st.caption("_CSV download is disabled by the `ENABLE_RAW_DATA_DOWNLOAD` environment variable._")


# ── Level 5: Real-time Model Prediction ───────────────────────────────────────

st.subheader("🤖 Real-time Usage Score Prediction")

if not MODEL_ENDPOINT_URL or not MODEL_API_KEY:
    st.info(
        "**Model API not configured.**  \n"
        "Set `MODEL_ENDPOINT_URL` and `MODEL_API_KEY` environment variables "
        "to enable live predictions.\n\n"
        "Find these values in **Models → Usage Score Predictor → Overview**.",
        icon="ℹ️",
    )
else:
    st.caption("Enter the number of active users to get a predicted usage score from the deployed model.")

    active_users_input = st.slider(
        "Active Users",
        min_value=0,
        max_value=1000,
        value=300,
        step=10,
    )

    if st.button("Predict Usage Score", type="primary"):
        with st.spinner("Calling model API..."):
            try:
                result = call_model(active_users_input)
                predicted_score = result.get("response", {}).get("usage_score", result.get("response"))
                st.success(f"**Predicted Usage Score: {predicted_score}**")
                col_a, col_b = st.columns(2)
                col_a.metric("Active Users (input)", active_users_input)
                col_b.metric("Predicted Score", predicted_score,
                             delta=f"{'▲ High Performer' if float(predicted_score) >= SCORE_ALERT_THRESHOLD else '▽ Below threshold'}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the model endpoint. Check `MODEL_ENDPOINT_URL`.", icon="🚫")
            except requests.exceptions.HTTPError as e:
                st.error(f"Model API returned an error: {e}", icon="🚫")
            except Exception as e:
                st.error(f"Unexpected error: {e}", icon="🚫")

st.divider()


# ── Footer ────────────────────────────────────────────────────────────────────

st.caption(
    f"Report generated at: `{summary['generated_at']}` · "
    f"Python `{summary['python_version']}` · "
    f"Source: `{CSV_PATH}`"
)
