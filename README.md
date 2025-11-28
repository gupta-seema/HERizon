# 🌐 **HERizon**

### **Safe automation, seamless escalation, and the end of the wait time**

HERizon is an enterprise-grade **multi-agent security and automation platform** designed to modernize IT operations, reduce backlog, and empower cybersecurity teams.

It uses **intelligent agent orchestration** to:

* Detect Shadow IT
* Automate security actions
* Score and map risks
* Streamline access governance
* Maintain human oversight for high-risk cases

Built using **Azure AI Foundry**, HERizon delivers both **speed** and **safety** across enterprise workflows.

---

## 🚀 **Key Features**

### **1. Shadow IT Detection & Automated Remediation**

HERizon integrates with **Microsoft Defender** and analyzes security logs using a structured multi-agent workflow:

| Agent                            | Purpose                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| **Defender Data Fetcher**        | Retrieves telemetry from Microsoft Defender APIs                     |
| **SaaS Detection Agent**         | Identifies unapproved SaaS tools or risky usage patterns             |
| **Risk Scoring Agent**           | Calculates risk score (0–100) + severity with detailed justification |
| **Policy Mapping Agent**         | Maps events to enterprise security & compliance rules                |
| **Automation Agent**             | Executes safe, reversible remediation actions                        |
| **Human Security Analyst Agent** | Performs expert review for high-risk or ambiguous cases              |

This pipeline enables **fast**, **automated**, and **safe** responses to potential security threats.

---

### **2. Intelligent Access Management Assistant**

Employees request access through a **chatbot interface**, and HERizon automatically:

* Verifies user identity and role
* Checks RBAC, entitlement, and policy compliance
* Auto-approves & provisions access when allowed
* Routes exceptions for human approval
* Generates audit logs
* Sends real-time notifications

This transforms access provisioning from **days to seconds** and reduces helpdesk load significantly.

---

## 🧠 **Agent Architecture**

HERizon uses Azure AI Foundry to orchestrate a chain of specialized agents.

| Agent Name                        | Purpose                                                             |
| --------------------------------- | ------------------------------------------------------------------- |
| **Defender Data Fetcher**         | Connects to Microsoft Defender and retrieves logs                   |
| **SaaS Detector Agent**           | Detects Shadow IT and suspicious software activity                  |
| **Risk Scoring Agent**            | Assigns risk score and category using policies + CVE data           |
| **Policy Mapping Agent**          | Maps events to compliance rules and determines allowed/denied state |
| **Automation Agent**              | Performs secure automated actions (revocations, alerts, approvals)  |
| **Human Security Analyst Agent**  | Validates high-risk outputs and handles exceptions                  |
| **IT Shadow (Main Orchestrator)** | Runs the full multi-agent workflow and coordinates execution        |

---

## 🏗️ **Architecture Overview**

```
Microsoft Defender
        ↓
Defender Data Fetcher
        ↓
SaaS Detection Agent
        ↓
Risk Scoring Agent
        ↓
Policy Mapping Agent
        ↓
Automation Agent
        ↓
Human Security Analyst Agent
        ↓
Final Output / Dashboard / UI
```

---
## **Live Demo**
Link : https://drive.google.com/file/d/1_XTzabIZBNCke5YKwoxYT34qrLd4rfje/view?usp=sharing
---
## 🧩 **Tech Stack**

* **Azure AI Foundry** (Multi-agent orchestration)
* **Microsoft Defender for Cloud Apps**
* **Python 3.10+**
* **Flask** (local testing UI)
* **Azure Identity SDK**
* **Azure Agents SDK**
* Optional: **Power BI** or **custom frontend** for dashboards

---

## ⚙️ **Installation & Setup**

### **1. Clone Repository**

```bash
git clone https://github.com/<your-username>/HERizon.git
cd HERizon
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure Azure Credentials**

HERizon uses:

* `DefaultAzureCredential`
* Azure AI Foundry project endpoint
* Main orchestrator agent ID

Add to `.env`:

```
AZURE_PROJECT_ENDPOINT=<your-endpoint>
MAIN_AGENT_ID=<main-agent-id>
```

### **4. Run the Local UI**

```bash
python3 app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

You can now chat with the main agent and watch the full workflow run in real time.

---

## 📊 **Output Format**

HERizon produces **structured JSON**, ideal for:

* Dashboards (Power BI, Grafana)
* SIEM ingestion
* Compliance reports
* SOC workflows

Sample output includes:

* Detected SaaS apps
* Risk score + category
* Policies triggered
* Actions performed
* User access decisions
* Escalations to human reviewers

---

## 🔒 **Security & Safety**

* Human-in-the-loop for high-risk cases
* Transparent, explainable actions
* Policy-aligned automation
* Audit logs for every agent decision
* No irreversible or destructive operations

---

## 🌱 **Roadmap**

* Power BI / Grafana dashboard
* Role-based UI
* ServiceNow / Jira integration
* Expansion to HR & Finance workflows
* Multilingual support
* Azure Lighthouse plugin

---

## 🤝 **Contributing**

Pull requests are welcome!
Open an issue first to discuss proposed changes or features.

---

## 🎓 **Created By — HERizon Team**

* **Seema Gupta**
* **Anayna Singh**
* **Sneha Joshi**
* **Meghana Rabba**
* **Deepali Budhiraja**

---

## 📄 **License**

MIT License 
