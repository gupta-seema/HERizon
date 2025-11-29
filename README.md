# 🌐 **HERizon**

### **Safe automation, seamless escalation, and the end of wait times**

HERizon is an enterprise-grade **multi-agent security and automation platform** built with **Azure AI Foundry** to modernize IT operations, eliminate backlog, and empower cybersecurity teams.

It uses intelligent agent orchestration to:

- Detect Shadow IT  
- Automate security actions  
- Score and map risks  
- Streamline access governance  
- Maintain human oversight for high-risk cases  

HERizon brings **speed**, **explainability**, and **enterprise safety** to cloud security workflows.

---

# 🧩 **HERizon Systems Overview**

HERizon contains **two distinct multi-agent subsystems**, each with its own orchestration logic but unified under one platform.

---

# 1️⃣ **Shadow IT Detection & Automated Remediation**

HERizon’s Shadow IT Detection & Automated Remediation system continuously monitors enterprise environments to identify unauthorized or risky SaaS applications. By combining real-time telemetry from Microsoft Defender with a multi-agent orchestration workflow, it automatically scores, maps, and remediates potential threats. High-risk or ambiguous cases are escalated to human analysts, ensuring that all actions are both fast and safe, while maintaining full compliance and auditability.

### **Shadow IT Pipeline**

| Agent                            | Purpose                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| **Defender Data Fetcher**        | Retrieves telemetry from Microsoft Defender                          |
| **SaaS Detection Agent**         | Detects unapproved SaaS usage patterns                               |
| **Risk Scoring Agent**           | Generates risk score (0–100) + severity justification                |
| **Policy Mapping Agent**         | Maps activity to enterprise policies                                 |
| **Automation Agent**             | Executes safe, reversible remediation                                |
| **Human Security Analyst Agent** | Reviews high-risk or ambiguous events                                |
| **IT Shadow (Orchestrator)**     | Manages the complete Shadow IT workflow                              |

This enables fast, automated, compliant responses to potential threats.

---

# 2️⃣ **Access Management Agent Suite (AMAS)**

AMAS automates software access provisioning using 8 coordinated agents.

### **AMAS Capabilities**

- Chatbot-based access requests  
- Role & policy-aware approval decisions  
- License and seat management  
- Duplicate-tool detection  
- Immutable audit logs  
- Automated provisioning through Azure AD (Entra ID)  
- Escalation for high-risk / policy exceptions  

### **AMAS Pipeline**

| Agent                         | Responsibility                                                                                   |
|------------------------------|---------------------------------------------------------------------------------------------------|
| **Role Classification Agent** | Maps job title + department → role category                                                      |
| **Risk Assessment Agent**     | Evaluates whether the tool fits the user's role; flags high-risk requests                        |
| **License Agent**             | Verifies seat availability                                                                       |
| **Knowledge Agent**           | Checks for duplicate tools already accessible to the user                                        |
| **Audit Agent**               | Writes immutable logs to CosmosDB                                                                |
| **Automation Agent**          | Grants/revokes access via Azure AD (Entra ID)                                                   |
| **Escalation Agent**          | Sends exceptions to managers via Logic Apps                                                     |
| **Main Orchestrator Agent**   | Connects all agents and controls full decision workflow                                          |

---

# 🧠 **Architectural Summary**

HERizon uses Azure AI Foundry for modular, extensible multi-agent orchestration.

### **Shadow IT Workflow**

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

### **AMAS Workflow**

```
User Request
        ↓
Role Classification Agent
        ↓
Risk Assessment Agent
        ↓
License Agent
        ↓
Knowledge Agent
        ↓
Automation Agent
        ↓
Escalation Agent (if needed)
        ↓
Audit Agent
        ↓
Main Orchestrator Agent
        ↓
Final Access Decision / Provisioning
```

---

# 🎥 **Live Demo**
https://drive.google.com/file/d/1_XTzabIZBNCke5YKwoxYT34qrLd4rfje/view?usp=sharing

---

# 🧩 **Tech Stack**

- Azure AI Foundry  
- Microsoft Defender for Cloud Apps  
- Python 3.10+  
- Flask (local testing UI)  
- Azure Identity SDK  
- Azure Agents SDK  
- Optional: Power BI / Custom frontend  

---

# ⚙️ **Installation & Setup**

## **1️⃣ Shadow IT Detection Setup**

### Clone Repository
```bash
git clone https://github.com/<your-username>/HERizon.git
cd HERizon
```

### Install Dependencies
```bash
pip install flask python-dotenv azure-identity azure-ai-projects
```

### Configure Azure Credentials

#### 1. Authenticate with Azure
```bash
az login
```

#### 2. Update orchestrator.py with your Azure credentials
Edit `orchestrator.py` and update:
```python
endpoint="https://<your-project>.services.ai.azure.com/api/projects/<your-project-id>"
MAIN_AGENT_ID = "<your-agent-id>"
```

To find your credentials:
1. Go to Azure AI Foundry (https://ai.azure.com)
2. Navigate to your project
3. Copy the **Project endpoint** URL
4. Navigate to your Shadow IT orchestrator agent and copy its **Agent ID**

### Run Local UI
```bash
python3 orchestrator.py
```

Browser:
```
http://127.0.0.1:5000
```

**Note**: The orchestrator will fail at startup if Azure credentials are not properly configured. Ensure you've run `az login` and that the endpoint/agent ID are correct.

---

## **2️⃣ AMAS Access Management Setup**

### Clone Repository
```bash
git clone https://github.com/<your-username>/HERizon.git
cd HERizon/azure_access_webapp/azure_access_webapp
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Azure Credentials
Create or update `.env` file in `azure_access_webapp/azure_access_webapp/`:
```
AZURE_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<your-project-id>
MAIN_AGENT_ID=<your-agent-id>
```

To find your credentials:
1. Go to Azure AI Foundry (https://ai.azure.com)
2. Navigate to your project
3. Copy the **Project endpoint** and **Agent ID** from your agents

### Run Local UI
```bash
cd azure_access_webapp/azure_access_webapp
python3 app.py
```

Browser:
```
http://127.0.0.1:5000
```

---

# 📊 **Output Format**

HERizon produces **structured JSON**, suitable for:

- SIEM ingestion  
- Power BI / Grafana dashboards  
- Compliance & audit reports  
- SOC workflows  

Includes:

- Detected SaaS apps  
- Risk score + rationale  
- Policy outcomes  
- Actions taken  
- Access approval decisions  
- Escalations  

---

# 🔒 **Security & Safety Controls**

- Human-in-the-loop for high-risk actions  
- Policy-aligned automation  
- Immutable audit logs  
- No destructive operations  

---

# 🌱 **Roadmap**

- Power BI / Grafana dashboards  
- Role-based UI  
- ServiceNow / Jira integration  
- HR & Finance automation agents  
- Multilingual support  
- Azure Lighthouse support  

---

# 🤝 **Contributing**

Pull requests welcome. Open an issue for discussion.

---

# 🎓 **HERizon Team**

- **Seema Gupta**  
- **Anayna Singh**  
- **Sneha Joshi**  
- **Meghana Rabba**  
- **Deepali Budhiraja**  

---

# 📄 **License**

MIT License

