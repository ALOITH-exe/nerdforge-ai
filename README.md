<div align="center">

# NerdForge AI

### AI-Powered Security Operations & Threat Intelligence Platform

**Simulate attacks. Analyze threats. Engineer detections. Investigate incidents.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ALOITH-exe/nerdforge-ai)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

[Live Demo](https://frontend-production-46e2.up.railway.app/) · [Report an Issue](https://github.com/ALOITH-exe/nerdforge-ai/issues) · [Repository](https://github.com/ALOITH-exe/nerdforge-ai)

</div>

---

## Overview

**NerdForge AI** is an AI-powered security operations platform designed to assist security analysts throughout the threat lifecycle — from **attack simulation and threat analysis to detection engineering and incident reporting**.

The platform combines Generative AI with established cybersecurity frameworks and tools to transform complex security scenarios into actionable intelligence.

NerdForge AI is built around a simple idea:

> **AI should augment security analysts, not replace them.**

Instead of treating an LLM as a generic chatbot, NerdForge AI uses AI-driven workflows to perform security-specific reasoning, structure attack scenarios, map adversary behavior to **MITRE ATT&CK**, extract indicators of compromise, generate detection logic, and produce investigation-ready reports.

### What NerdForge AI Does

```text
                    ┌──────────────────────┐
                    │      Security Team    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     NerdForge AI     │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   Attack Simulation      Threat Analysis     Incident Response
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Detection Engineering│
                    └──────────┬───────────┘
                               ▼
                    Sigma / YARA / IDS Rules
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Investigation Report │
                    └──────────────────────┘
```

---

## Key Capabilities

### Attack Scenario Generation

Generate structured, realistic attack scenarios based on parameters such as:

* Industry
* Attack type
* Operating system
* Environment
* Difficulty
* Custom scenario requirements

Supported scenarios can include:

* Ransomware
* Phishing
* Credential theft
* Data exfiltration
* Initial access
* Persistence
* Privilege escalation
* Command and control
* Advanced persistent threat scenarios

Each generated scenario can include attack stages, timelines, events, TTPs, and MITRE ATT&CK mappings.

---

### AI SOC Analyst

NerdForge AI provides an AI-assisted investigation layer for security analysts.

Capabilities include:

* Security event interpretation
* Attack-chain reconstruction
* Threat severity assessment
* Contextual explanations
* Suspicious activity analysis
* Recommended response actions
* Analyst-oriented investigation summaries

The objective is to reduce the amount of repetitive analysis required during alert triage while keeping the analyst in control of the final decision.

---

### Threat Intelligence & IOC Analysis

Extract and analyze indicators of compromise from security events and generated scenarios.

Supported IOC categories include:

| IOC Type      | Examples                        |
| ------------- | ------------------------------- |
| IP Addresses  | IPv4 / IPv6 addresses           |
| Domains       | Malicious or suspicious domains |
| URLs          | Phishing / payload URLs         |
| File Hashes   | MD5 / SHA1 / SHA256             |
| Registry Keys | Windows persistence indicators  |
| File Paths    | Suspicious executable locations |
| Processes     | Malicious process activity      |

External intelligence sources can be used to enrich indicators and provide additional context.

Current integrations include:

* VirusTotal
* AbuseIPDB

---

### Detection Engineering

Convert analyzed threats into detection content.

NerdForge AI can assist in generating:

* **Sigma rules**
* **YARA rules**
* **Snort rules**
* **Suricata rules**

The goal is to bridge the gap between:

```text
Threat
  ↓
Investigation
  ↓
Observed TTPs
  ↓
Detection Logic
  ↓
Deployable Security Rule
```

This allows an analyst to move from understanding an attack to creating defensive controls within the same workflow.

---

### Automated Incident Reporting

Generate structured incident reports containing:

* Executive summary
* Incident overview
* Technical analysis
* Attack timeline
* MITRE ATT&CK mapping
* Indicators of compromise
* Severity assessment
* Recommended actions
* Detection opportunities

Reports can be exported for use by both technical security teams and non-technical stakeholders.

---

### AI Tutor Mode

NerdForge AI also includes an educational workflow designed to help cybersecurity learners understand offensive and defensive security concepts.

The AI Tutor can explain:

* Attack techniques
* MITRE ATT&CK techniques
* Security events
* Detection logic
* Malware behavior
* Incident-response decisions
* Generated attack scenarios

This makes the platform useful not only for SOC workflows, but also for cybersecurity education and hands-on training.

---

# Architecture

NerdForge AI follows a modular architecture separating the presentation layer, API layer, AI orchestration, security intelligence, and persistence.

```text
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│                         React + TypeScript                      │
│                                                                 │
│  Scenario Generator │ SOC Dashboard │ MITRE │ Reports │ Tutor  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ REST API
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API LAYER                               │
│                           FastAPI                               │
│                                                                 │
│  Authentication / Validation / Routing / Business Logic         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AI ORCHESTRATION                            │
│                                                                 │
│       LangChain                     LangGraph                   │
│          │                              │                       │
│          └──────────────┬───────────────┘                       │
│                         │                                       │
│              ┌──────────┴──────────┐                            │
│              ▼                     ▼                            │
│           Groq API            Google Gemini                     │
└─────────────────────────────────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌────────────────────┐
│ Threat Intel    │   │ Security        │   │ Attack Simulation  │
│                 │   │ Frameworks      │   │                    │
│ VirusTotal      │   │ MITRE ATT&CK    │   │ Atomic Red Team     │
│ AbuseIPDB       │   │ Sigma           │   │ MCP Integrations   │
└─────────────────┘   │ YARA            │   └────────────────────┘
                      │ Snort/Suricata   │
                      └─────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │       DATABASE         │
                    │                        │
                    │ SQLite / PostgreSQL    │
                    └────────────────────────┘
```

---

# Technology Stack

## Backend

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Core backend language              |
| FastAPI    | REST API framework                 |
| SQLAlchemy | Database ORM                       |
| SQLite     | Local development database         |
| PostgreSQL | Production database option         |
| Pydantic   | Data validation                    |
| LangChain  | LLM application framework          |
| LangGraph  | Stateful AI workflow orchestration |

## AI

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| Groq          | Fast LLM inference            |
| Google Gemini | High-quality generative AI    |
| LangChain     | Model/tool orchestration      |
| LangGraph     | Multi-step security workflows |

## Frontend

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| React         | UI framework                   |
| TypeScript    | Type-safe frontend development |
| Vite          | Frontend build tooling         |
| Tailwind CSS  | UI styling                     |
| Framer Motion | Interface animations           |
| Recharts      | Data visualization             |

## Security Ecosystem

| Technology      | Purpose                            |
| --------------- | ---------------------------------- |
| MITRE ATT&CK    | Adversary behavior and TTP mapping |
| Atomic Red Team | Attack simulation                  |
| Sigma           | SIEM detection rules               |
| YARA            | Malware detection rules            |
| Snort           | Network intrusion detection        |
| Suricata        | Network threat detection           |
| VirusTotal      | IOC enrichment                     |
| AbuseIPDB       | IP reputation intelligence         |

---

# Project Structure

```text
nerdforge-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│
├── .gitignore
├── LICENSE
└── README.md
```

---

# Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.11+
* Node.js 18+
* npm
* Git

API credentials may also be required for:

* Groq
* Google Gemini
* VirusTotal
* AbuseIPDB

---

## 1. Clone the Repository

```bash
git clone https://github.com/ALOITH-exe/nerdforge-ai.git
cd nerdforge-ai
```

---

## 2. Configure the Backend

```bash
cd backend

python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

On Windows, create `.env` manually if `cp` is unavailable.

Configure the required API credentials inside `.env`.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

VIRUSTOTAL_API_KEY=your_virustotal_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_api_key

DATABASE_URL=sqlite:///./nerdforge.db
```

**Never commit `.env` or API credentials to Git.**

---

## 3. Start the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## 4. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# API

NerdForge AI exposes a REST API through FastAPI.

## Health Check

```http
GET /api/health
```

Used to verify backend availability.

---

## Generate Attack Scenario

```http
POST /api/attacks/generate
```

Example request:

```json
{
  "name": "Finance Ransomware Simulation",
  "industry": "finance",
  "attack_type": "ransomware",
  "difficulty": "Medium",
  "operating_system": "Windows",
  "environment": "On-Premise"
}
```

Example response:

```json
{
  "id": "attack-uuid",
  "name": "Finance Ransomware Simulation",
  "status": "completed",
  "created_at": "timestamp",
  "attack_stages": [],
  "timeline": [],
  "events": [],
  "analysis": {}
}
```

---

## List Attack Scenarios

```http
GET /api/attacks/
```

---

## Retrieve Attack Scenario

```http
GET /api/attacks/{id}
```

---

## Interactive API Documentation

When running locally, FastAPI automatically provides:

```text
http://localhost:8000/docs
```

and:

```text
http://localhost:8000/redoc
```

---

# Example Workflow

A typical NerdForge AI workflow looks like this:

### 1. Define the Scenario

An analyst selects:

```text
Industry:       Finance
Attack Type:    Ransomware
OS:             Windows
Environment:    On-Premise
Difficulty:     Medium
```

### 2. Generate the Attack Model

The AI creates:

* Attack stages
* Tactics and techniques
* Timeline
* Security events
* Adversary behavior

### 3. Map the Activity

Relevant behavior is mapped to:

**MITRE ATT&CK**

```text
Initial Access
      ↓
Execution
      ↓
Persistence
      ↓
Privilege Escalation
      ↓
Defense Evasion
      ↓
Command & Control
      ↓
Impact
```

### 4. Analyze the Threat

NerdForge AI evaluates:

* Suspicious behavior
* Indicators
* Attack progression
* Severity
* Potential impact

### 5. Engineer Detections

The system can generate:

```text
Sigma
YARA
Snort
Suricata
```

detection logic based on the observed behavior.

### 6. Generate the Report

The final investigation can be converted into a structured security report containing technical and executive-level findings.

---

# Security Considerations

NerdForge AI is designed as a **security research, education, and analyst-assistance platform**.

Important considerations:

* Never expose API keys in source code.
* Keep `.env` excluded through `.gitignore`.
* Use environment variables for secrets.
* Restrict CORS origins in production.
* Apply authentication before exposing sensitive endpoints publicly.
* Apply rate limiting to AI-backed endpoints.
* Validate and sanitize user-provided input.
* Do not execute generated attack commands against systems without authorization.
* Use isolated environments for attack simulation.
* Treat AI-generated security recommendations as analyst assistance rather than authoritative decisions.

### Responsible Use

Attack simulation and security testing functionality should only be used against systems and environments where you have explicit authorization.

---

# Deployment

The production frontend is currently deployed on **Railway**.

### Live Application

**https://frontend-production-46e2.up.railway.app/**

For production deployment, the recommended architecture is:

```text
                  Internet
                     │
                     ▼
              ┌──────────────┐
              │ Reverse Proxy│
              │ / Load Bal.  │
              └──────┬───────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      Frontend               FastAPI
       React                  Backend
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
          PostgreSQL         LLM APIs        Threat Intel
```

Production deployments should use HTTPS, secret management, restricted CORS, authentication, logging, monitoring, and appropriate API rate limits.

---

# Testing

## Backend

Run the backend and validate the API through:

```text
http://localhost:8000/docs
```

Test scenarios should include:

| Scenario                  | Expected Result                   |
| ------------------------- | --------------------------------- |
| Basic ransomware scenario | Structured attack scenario        |
| Phishing scenario         | Phishing-specific TTPs            |
| Custom scenario           | AI uses supplied scenario context |
| Different industry        | Industry-specific attack behavior |
| Invalid request           | Validation error                  |
| Missing API key           | Controlled configuration error    |

---

# Roadmap

NerdForge AI is actively extensible. Planned improvements include:

* [ ] Real-time security event ingestion
* [ ] Wazuh integration
* [ ] Elastic / ELK integration
* [ ] Splunk integration
* [ ] SIEM alert ingestion
* [ ] Automated alert correlation
* [ ] IOC relationship graphs
* [ ] ATT&CK Navigator integration
* [ ] Expanded threat-intelligence providers
* [ ] Detection-rule validation
* [ ] Automated rule testing
* [ ] Case management
* [ ] Analyst feedback loops
* [ ] Role-based access control
* [ ] Authentication and authorization
* [ ] Production-grade PostgreSQL deployment
* [ ] Security audit logging
* [ ] Containerized deployment
* [ ] Kubernetes support
* [ ] Expanded SOAR integrations

---

# Project Status

| Component                  | Status      |
| -------------------------- | ----------- |
| Backend API                | Complete    |
| AI Integration             | Complete    |
| Attack Scenario Generation | Complete    |
| MITRE ATT&CK Mapping       | Complete    |
| Threat Intelligence        | Implemented |
| Detection Engineering      | Implemented |
| Incident Reporting         | Implemented |
| AI Tutor                   | Implemented |
| Frontend                   | Complete    |
| Deployment                 | Live        |
| SIEM Integrations          | Roadmap     |
| SOAR Integrations          | Roadmap     |

---

# Team

Built by the NerdForge AI team for the **Digital Youth Leadership Program (DYLP) Vibe Coding Hackathon 2026**.

| Contributor         | Role                                 |
| ------------------- | ------------------------------------ |
| **Aftab Ahmed**     | Backend Development & AI Integration |
| **Ali Hamza**       | Deployment & DevOps                  |
| **Muhammad Raheel** | Frontend Development                 |

---

# Why NerdForge AI?

Traditional security workflows often require analysts to move between multiple tools:

```text
SIEM
 ↓
Threat Intelligence
 ↓
MITRE ATT&CK
 ↓
Detection Engineering
 ↓
Incident Documentation
 ↓
Reporting
```

NerdForge AI aims to bring these activities into a unified AI-assisted workflow.

The long-term vision is to evolve the platform from an AI-assisted security analysis tool into a **security operations orchestration layer** capable of connecting telemetry, threat intelligence, detection engineering, investigation, and response.

---

# Contributing

Contributions are welcome.

To contribute:

```bash
git clone https://github.com/ALOITH-exe/nerdforge-ai.git
cd nerdforge-ai
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them, and submit a pull request.

Please ensure that:

* Secrets are never committed.
* New functionality includes appropriate tests.
* Security-sensitive changes are documented.
* Code follows the existing project structure.
* Pull requests clearly describe the change and its purpose.

---

# License

NerdForge AI is released under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

# Acknowledgments

NerdForge AI builds upon the work of several projects and organizations across the cybersecurity and AI ecosystem:

* [MITRE ATT&CK](https://attack.mitre.org/)
* [Atomic Red Team](https://atomicredteam.io/)
* [Sigma](https://sigmahq.io/)
* [YARA](https://virustotal.github.io/yara/)
* [Snort](https://www.snort.org/)
* [Suricata](https://suricata.io/)
* [VirusTotal](https://www.virustotal.com/)
* [AbuseIPDB](https://www.abuseipdb.com/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [LangChain](https://www.langchain.com/)
* [LangGraph](https://www.langchain.com/langgraph)
* [Groq](https://groq.com/)
* [Google Gemini](https://ai.google.dev/)

---

<div align="center">

### Built for Security. Powered by AI.

**NerdForge AI — Turning Threat Intelligence into Action.**

If you find the project useful, consider giving the repository a ⭐

</div>
