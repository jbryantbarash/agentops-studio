import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="AgentOps Studio", layout="wide")

st.title("🟦 AgentOps Studio")
st.caption("A safe, local AI agent builder and execution sandbox for enterprise workflows.")

# ----------------------------
# Sidebar: Agent Settings
# ----------------------------
st.sidebar.header("🛠️ Agent Builder")

agent_name = st.sidebar.text_input("Agent Name", "Invoice Reconciliation Agent")

allowed_actions = st.sidebar.multiselect(
    "Allowed Actions",
    ["read", "classify", "update", "summarize"],
    default=["read", "classify"],
    help="These are the actions the agent is allowed to simulate.",
)

forbidden_actions = st.sidebar.multiselect(
    "Forbidden Actions",
    ["delete", "external_api", "write_sensitive"],
    default=["delete", "external_api"],
    help="These actions will always be blocked in the sandbox.",
)

safety_limit = st.sidebar.number_input(
    "Max Rows Agent Can Modify",
    min_value=10,
    max_value=5000,
    value=100,
    step=10,
    help="Soft safety constraint for simulated updates.",
)

threshold = st.sidebar.number_input(
    "High Value Threshold",
    min_value=0,
    max_value=1_000_000,
    value=500,
    step=50,
    help="Values above this in the selected column will be marked 'High Value'.",
)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload Workbook/CSV", type=["csv"])

# ----------------------------
# Agent Blueprint Builder
# ----------------------------
st.subheader("1. Agent Blueprint")

blueprint = {
    "agent_name": agent_name,
    "allowed_actions": allowed_actions,
    "forbidden_actions": forbidden_actions,
    "safety_constraints": {
        "max_rows": int(safety_limit),
        "review_changes": True,
    },
    "threshold": int(threshold),
    "timestamp": str(datetime.utcnow()),
}

st.markdown("#### Current Agent Configuration")
st.json(blueprint)

st.download_button(
    "⬇️ Download Agent Blueprint",
    data=json.dumps(blueprint, indent=4),
    file_name=f"{agent_name.replace(' ', '_').lower()}_blueprint.json",
    mime="application/json",
)

st.markdown("---")

# ----------------------------
# Agent Testing Sandbox
# ----------------------------
st.subheader("2. Agent Execution Sandbox")

if uploaded_file:
    # First read attempt
    df = pd.read_csv(uploaded_file)

    # If pandas thinks there's only one column, try to split it on commas manually
    if len(df.columns) == 1:
        col_name = df.columns[0]
        first_value = str(df.iloc[0, 0]) if len(df) > 0 else ""

        # If the header or first value contains commas, assume it's a "squashed" CSV
        if "," in col_name or "," in first_value:
            uploaded_file.seek(0)  # reset file pointer
            raw_df = pd.read_csv(uploaded_file, header=None)

            # Split the single column on commas into multiple columns
            split_df = raw_df[0].astype(str).str.split(",", expand=True)

            # First row is header, remaining rows are data
            split_df.columns = split_df.iloc[0]
            df = split_df[1:].reset_index(drop=True)

    st.markdown("#### Data Preview")
    st.dataframe(df.head())

    columns = df.columns.tolist()
    if not columns:
        st.error("No columns found in this file.")
    else:
        value_col = st.selectbox(
            "Select column to use for value-based classification",
            columns,
            index=1 if len(columns) > 1 else 0,
            help="This column will be converted to numeric for High/Low classification.",
        )

        test_prompt = st.text_area(
            "Test Prompt",
            "Reconcile high-value records and highlight items over the selected threshold.",
        )

        run_clicked = st.button("▶ Run Agent in Sandbox")

        if run_clicked:
            actions = []
            sim_df = df.copy()

            # READ
            if "read" in allowed_actions:
                actions.append("Read dataset (previewed first few rows).")

            # CLASSIFY
            classified = False
            if "classify" in allowed_actions:
                # Force column to numeric
                numeric_series = pd.to_numeric(sim_df[value_col], errors="coerce")
                sim_df["Classification"] = numeric_series.apply(
                    lambda x: "High Value"
                    if pd.notna(x) and x > threshold
                    else "Low/Unknown"
                )
                actions.append(
                    f"Classified rows based on `{value_col} > {threshold}` as 'High Value', else 'Low/Unknown'."
                )
                classified = True

            # UPDATE (simulated)
            if "update" in allowed_actions:
                modified_rows = min(len(sim_df), safety_limit)
                actions.append(
                    f"Simulated updating up to {modified_rows} rows (within safety constraints)."
                )

            # SUMMARIZE (simulated)
            if "summarize" in allowed_actions:
                actions.append(
                    "Simulated generating a high-level summary of the dataset and agent actions."
                )

            # ------------------------
            # Action Log
            # ------------------------
            st.markdown("### ✅ Action Log")
            if actions:
                for a in actions:
                    st.write(f"✔️ {a}")
            else:
                st.write("No actions executed. Check your allowed actions configuration.")

            # ------------------------
            # Blocked Actions
            # ------------------------
            st.markdown("### 🛡️ Blocked Actions")
            if forbidden_actions:
                for f in forbidden_actions:
                    st.write(f"❌ Attempt blocked by policy: `{f}`")
            else:
                st.write("No actions are currently blocked by policy.")

            # ------------------------
            # Resulting Data Preview
            # ------------------------
            st.markdown("### 📊 Resulting Data (Simulation)")
            st.dataframe(sim_df.head())

            if classified:
                st.success(
                    f"Classification complete using column `{value_col}` and threshold {threshold}. "
                    "Look for the 'Classification' column in the Resulting Data above."
                )
else:
    st.info("Upload a CSV in the sidebar to test this agent in the sandbox.")
