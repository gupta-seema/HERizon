🌐 HERizon
Safe automation, seamless escalation, and the end of the wait time

HERizon is an enterprise-grade multi-agent security and automation platform designed to modernize IT operations, reduce backlog, and empower cybersecurity teams.
It uses intelligent agent orchestration to handle Shadow IT detection, automated security actions, and access governance — all while maintaining human oversight for high-risk cases.

🚀 Key Features
1. Shadow IT Detection & Automated Remediation

HERizon integrates with Microsoft Defender and analyzes security logs using a structured workflow of agents:

Defender Data Fetcher — retrieves logs and telemetry

SaaS Detection Agent — identifies unapproved apps or risky usage

Risk Scoring Agent — calculates severity (0–100) + justification

Policy Mapping Agent — maps events to enterprise security policies

Automation Agent — performs safe, policy-driven remediation

Human Security Analyst Agent — final expert validation for complex cases

This enables fast, automated, and safe responses to potential threats.

2. Intelligent Access Management Assistant

Employees request access using a chatbot. HERizon then:

Verifies identity and role

Checks entitlement and RBAC compliance

Auto-approves and provisions allowed access

Routes exceptions for approval

Generates audit logs

Provides real-time notifications

This reduces helpdesk load and speeds access provisioning from days to seconds.

🧠 Agent Architecture

HERizon uses Azure AI Foundry to orchestrate a chain of specialized agents:

Agent Name	Purpose
Defender Data Fetcher	Connects to Microsoft Defender API and retrieves logs.
SaaS Detector Agent	Identifies Shadow IT activity or suspicious software usage.
Risk Scoring Agent	Assigns a risk score & category using policy + CVE context.
Policy Mapping Agent	Maps events to compliance rules and allowed/denied states.
Automation Agent	Executes safe remediations and access actions.
Human Security Analyst Agent	Reviews high-risk cases for safety/accuracy.
IT Shadow (Main Orchestrator)	Chains the workflow and coordinates agent execution.
🏗️ Architecture Diagram
Microsoft Defender  →  Defender Data Fetcher  
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
                       Final Output / UI

🧩 Tech Stack

Azure AI Foundry (multi-agent orchestration)

Microsoft Defender for Cloud Apps

Flask (testing UI for agent interaction)

Python 3.10+

Azure Identity SDK

Azure Agents SDK

Optional: Power BI dashboard / custom frontend for visualization

⚙️ Installation & Setup
1. Clone Repository
git clone https://github.com/<your-username>/HERizon.git
cd HERizon

2. Install Dependencies
pip install -r requirements.txt

3. Configure Azure Credentials

HERizon uses:

DefaultAzureCredential

Your Azure AI Foundry project endpoint

Your Main Agent ID

Update your .env file:

AZURE_PROJECT_ENDPOINT=<your-endpoint>
MAIN_AGENT_ID=<main-agent-id>

▶️ Run the Local UI
python3 app.py


Open:

http://127.0.0.1:5000


You can now chat with the main agent and watch the workflow execute in real time.

📊 Outputs

HERizon produces structured JSON that can be fed into:

Dashboards

SIEM tools

Compliance reports

SOC workflows

Sample output includes:

Detected SaaS apps

Risk scores

Policy decisions

Automated actions executed

Escalations made

Final security analyst summaries

🔒 Security & Safety

HERizon ensures:

Human-in-the-loop for high-risk cases

Transparent and auditable decisions

Policy-aligned automation

No unsafe self-escalation or destructive actions

🌱 Roadmap

 Power BI / Grafana dashboards

 Role-based frontend

 Integration with ServiceNow or Jira

 HR & Finance workflow agent expansions

 Multilingual support

 Plugin for Azure Lighthouse environments

🤝 Contributing

Pull requests are welcome!
Please open an issue first to discuss your ideas.

🎓 Created By

HERizon Team
Seema Gupta

Anayna Singh

Sneha Joshi

Meghana Rabba

Deepali Budhiraja

📄 License

MIT License (or your preferred license)