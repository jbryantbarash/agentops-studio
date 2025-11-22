import streamlit as st
import pandas as pd
import json
from datetime import datetime

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
    default=["read", "classify"]
)

forbidden_actions = st.sidebar.multiselect(
    "Forbidden Actions",
    ["delete", "external_api", "write_sensitive"],
    default=["delete", "external_api"]
)

safety_limit = st.sidebar.number_input("Max Rows Agent Can Modify", 100, 5000, 100)

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
        "review_changes": True
    },
    "timestamp": str(datetime.utcnow())
}

st.json(blueprint)

st.download_button(
    "Download Agent Blueprint",
    data=json.dumps(blueprint, indent=4),
    file_name=f"{agent_name.replace(' ','_')}_blueprint.json",
    mime="application/json"
)

st.markdown("---")

# ----------------------------
# Agent Testing Sandbox
# ----------------------------
st.subheader("2. Agent Execution Sandbox")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df.head())

    test_prompt = st.text_area("Test Prompt", "Reconcile invoices over $500.")

    if st.button("Run Agent in Sandbox"):
        actions = []

        # Example: simulate "classification"
        if "classify" in allowed_actions:
            df["Classification"] = df[df.columns[1]].apply(
                lambda x: "High Value" if x > 500 else "Low Value"
            )
            actions.append("Classified rows based on Amount > $500")

        # Example: simulate "update" action
        if "update" in allowed_actions:
            modified_rows = min(len(df), safety_limit)
            actions.append(f"Updated {modified_rows} rows (within safety constraints)")

        st.markdown("### Action Log")
        for a in actions:
            st.write(f"✔️ {a}")

        # Safety enforcement
        st.markdown("### Blocked Actions")
        for f in forbidden_actions:
            st.write(f"❌ Attempt blocked: {f}")

else:
    st.info("Upload a CSV to test the agent.")
