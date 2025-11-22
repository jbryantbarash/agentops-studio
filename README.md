# 🟦 AgentOps Studio  
### Safe AI Agent Builder & Execution Sandbox

AgentOps Studio is a lightweight, local prototype demonstrating how enterprise AI agents can be **safely created, tested, monitored, and shared** — without exposing data or enabling uncontrolled actions.

This project mirrors how modern enterprise platforms are evolving toward **trusted, action-capable AI agents** with explicit permission boundaries, transparent action logs, and safe execution environments.

---

## 🚀 What This Project Demonstrates

AgentOps Studio shows your ability to:

- Architect safe AI agent frameworks  
- Build permission-based action systems  
- Simulate and monitor agent behavior  
- Design enterprise-grade constraints (zero leakage, explicit allowed/blocked actions)  
- Create reusable agent blueprints  
- Think like an AI transformation leader

This is the type of prototype used during:

- Enterprise AI strategy engagements  
- Agent governance design  
- POC scoping  
- Human-in-the-loop safety reviews  
- Controlled deployment of internal AI automations  

---

## ✨ Features

### 🧠 Agent Builder
Create an agent with:

- Name  
- Allowed actions  
- Forbidden actions  
- Safety constraints (max rows, review-on-change)
- Data sources (CSV/workbook)

Output: a **shareable agent blueprint JSON file**.

---

### 🧪 Execution Sandbox
Test your agent against real data in a safe simulation:

- Action-by-action log  
- Permission enforcement  
- No external calls  
- No persistent writes  
- Preview all changes before approval  

---

### 📦 Agent Blueprint Export
Export the agent as JSON:

```json
{
  "agent_name": "Invoice Reconciliation Agent",
  "allowed_actions": ["read", "classify"],
  "forbidden_actions": ["delete", "external_api"],
  "safety_constraints": {
    "max_rows": 100,
    "review_changes": true
  },
  "timestamp": "2025-01-01"
}

🛠 Tech Stack

Streamlit

Python

Pandas

JSON agent schemas

Local execution only (zero data leakage)

## 🚀 Clone & Run

### 1. Clone the repository

```bash
git clone git@github.com:jbryantbarash/agentops-studio.git
cd agentops-studio
```

### 2. (Optional) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch AgentOps Studio
```bash
streamlit run app.py
```

