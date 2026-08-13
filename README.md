<div align="center">

# NerdForge AI

### *Autonomous AI-Powered Security Operations Center*

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.139.0-green)
![React](https://img.shields.io/badge/react-18.2.0-blue)
![Tailwind](https://img.shields.io/badge/tailwind-3.4.0-38bdf8)
![License](https://img.shields.io/badge/license-MIT-yellow)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Live Demo](https://img.shields.io/badge/demo-live-success)

</div>

---

## 📋 **Table of Contents**

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Tech Stack](#-tech-stack)
- [API Endpoints](#-api-endpoints)
- [Project Status](#-project-status)
- [Team](#-team)
- [License](#-license)

---

## 🎯 **Overview**

**NerdForge AI** is an autonomous, AI-powered Security Operations Center (SOC) platform that combines **attack simulation, threat detection, incident response, and automated reporting** into a single intelligent ecosystem.

Built for the **DYLP Vibe Coding Hackathon 2026**, this project demonstrates how Generative AI can augment security analysts, making cybersecurity operations faster, more accessible, and more effective.

> *"The future of cybersecurity isn't about replacing analysts—it's about augmenting them with AI superpowers."*

🔗 **Live Demo:** [https://frontend-production-46e2.up.railway.app/](https://frontend-production-46e2.up.railway.app/)

---

## ✨ **Key Features**

### 🔴 **AI Attack Generation**
- Generate realistic cyberattacks (ransomware, phishing, APT, data exfiltration)
- MITRE ATT&CK technique mapping
- Realistic attack timelines and TTPs

### 🔵 **AI SOC Analyst**
- Natural language explanations of security events
- Attack chain reconstruction
- Severity scoring and prioritization
- Recommended response actions

### 🧠 **Threat Intelligence**
- IOC extraction (IPs, domains, hashes, registry keys)
- Threat intelligence enrichment (VirusTotal, AbuseIPDB)
- Risk scoring (0-100)

### 🛡️ **Detection Engineering**
- Generate Sigma rules for SIEM platforms
- Generate YARA rules for malware detection
- Generate Snort/Suricata rules
- Production-ready rule export

### 📊 **Automated Incident Reporting**
- Executive summary
- Technical analysis
- MITRE mapping
- Recommendations
- PDF export

### 🎓 **AI Tutor Mode**
- Educational explanations of attack techniques
- Learning tool for cybersecurity students
- Interactive attack analysis

---

## 🏗️ **Architecture**
┌─────────────────────────────────────────────────────────────────┐
│ User Interface (React) │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│ │Scenario │ │ SOC │ │ MITRE │ │ Reports │ │
│ │Generator │ │Dashboard │ │ Matrix │ │ │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ API Gateway (FastAPI) │
└─────────────────────────────────────────────────────────────────┘
│
┌────────────────────┼────────────────────┐
▼ ▼ ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│ Attack Planner │ │ SOC Analyst │ │ Detection Engineer │
│ (LangGraph) │ │ (LangGraph) │ │ (LangChain) │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
│ │ │
▼ ▼ ▼
┌─────────────────────────────────────────────────────────────────┐
│ LLM Orchestration Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│ │ Gemini │ │ Groq │ │ HackerAI │ │ Atomic Red Team │ │
│ │ 2.5 Flash│ │ Llama │ │ Clients │ │ MCP Server │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

text

---

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.11+
- Node.js 18+
- Git

### **Backend Setup**

```bash
# Clone the repository
git clone https://github.com/ALOITH-exe/nerdforge-ai.git
cd nerdforge-ai

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys (Groq, Gemini)
Frontend Setup
bash
# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
Run the Application
bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
Access
Service	URL
Backend API	http://localhost:8000
API Docs	http://localhost:8000/docs
Frontend	http://localhost:5173
🛠️ Tech Stack
Backend
Technology	Purpose
FastAPI	High-performance REST API
Python 3.14	Core language
SQLAlchemy	ORM for database models
SQLite/PostgreSQL	Database
Groq API	Primary LLM (fast responses)
Google Gemini API	Fallback LLM (high quality)
LangChain	Agent orchestration
LangGraph	Agent workflow management
Frontend
Technology	Purpose
React	UI framework
TypeScript	Type safety
Vite	Build tool
Tailwind CSS	Styling
Framer Motion	Animations
Recharts	Data visualization
Security Intelligence
Tool	Purpose
MITRE ATT&CK	Threat framework mapping
Atomic Red Team	Real attack simulations
SigmaHQ Rules	Detection rule repository
VirusTotal	IOC enrichment
📡 API Endpoints
Attack Generation
http
POST /api/attacks/generate
Request:

json
{
  "name": "Ransomware Test",
  "industry": "finance",
  "attack_type": "ransomware",
  "difficulty": "Medium",
  "operating_system": "Windows",
  "environment": "On-Premise"
}
Response:

json
{
  "id": "uuid",
  "name": "Attack Name",
  "status": "completed",
  "created_at": "timestamp",
  "attack_stages": [...],
  "timeline": [...],
  "events": [...],
  "analysis": {...}
}
List Attacks
http
GET /api/attacks/
Get Attack Details
http
GET /api/attacks/{id}
Health Check
http
GET /api/health
🧪 Testing
Manual Testing
Start the server: uvicorn app.main:app --reload

Open: http://localhost:8000/docs

Test endpoints with different inputs

Test Cases
Test Case	Input	Expected Output
Basic Attack	industry: finance, type: ransomware	Attack with MITRE stages
Custom Scenario	custom_scenario: "Phishing attack"	Uses custom text
Different Industry	industry: healthcare	Industry-specific scenario
📊 Project Status
Phase	Status
Backend	✅ Complete
AI Integration	✅ Complete
Frontend	✅ Complete
Deployment	✅ Live on Railway
🔒 Security
✅ .env protected with .gitignore

✅ .env.example template for team

✅ API keys never exposed

✅ CORS configured for frontend-backend communication

✅ Rate limit handling with retry logic

🤝 Team
Name	Role	GitHub
Aftab Ahmed	Backend Developer	ALOITH-exe
Ali Hamza	Deployment & DevOps	-
Muhammad Raheel	Frontend Developer	-
📚 Documentation
API Docs: http://localhost:8000/docs

Project Overview: CLAUDE.md

Setup Instructions: README.md

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgments
Groq for fast, accessible AI inference

Google Gemini for high-quality LLM capabilities

MITRE for the ATT&CK framework

Atomic Red Team for real-world attack simulations

FastAPI for excellent Python API framework

Digital Youth Leadership Program (DYLP) for organizing Vibe Coding 2026

<div align="center">
Built with ❤️ for the DYLP Vibe Coding Hackathon 2026

⭐ If you find this project useful, please give it a star! ⭐

</div> ```
