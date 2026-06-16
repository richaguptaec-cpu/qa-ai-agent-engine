# AI-Driven Quality Engineering Agent Studio 🧠🤖

A production-ready, highly scalable AI Testing Agent designed to automatically parse raw User Stories and generate comprehensive functional, technical, and non-functional test matrices. Built using **Google Gemini 2.5 Flash**, **Pydantic**, and **Streamlit**, this project demonstrates how to implement a deterministic, shift-left AI pipeline for modern Quality Engineering.

---

## 🚀 Key Engineering Capabilities

Unlike simple prompt wrappers, this agent functions as a context-aware QA colleague by enforcing standard QA methodologies and architectural boundaries:

* **Deterministic Output Contracts:** Utilizes Pydantic schemas to force the LLM to output structured data types (JSON), completely eliminating unstructured hallucinations and ensuring down-stream data parsing readiness.
* **Business Validation Parsing:** Automatically extracts clean, formalized Acceptance Criteria from unstructured stakeholder inputs.
* **Comprehensive Boundary Testing Matrix:** The agent evaluates conditions through multiple specialized QA vectors:
    * **Positive Scenarios:** Happy path functional validation.
    * **Negative Scenarios:** Graceful error handling, input sanitization, and workflow breaking.
    * **Edge Cases:** Boundary Value Analysis (BVA) and extreme conditions.
    * **Security Scenarios:** RBAC, unauthorized endpoint access, and token expirations.
    * **Application Security (AppSec):** Targeted SQL Injection vulnerabilities and data safety vectors.
    * **Infrastructure Conditions:** System performance under simulated network latency, timeouts, and race conditions.

---

## 🏗️ Extensible & Scalable Architecture

The system is designed following a **Modular Pipeline Pattern**. The scenario extraction engine is completely decoupled from the visualization frontend and output models.

[ Raw User Story Input ] ──> [ QA Agent Engine (Gemini) ] ──> [ Pydantic Type Enforcement ] ──> [ JSON Data Stream ]
│
┌───────────────────────────────────────────────────────┤
▼                                                       ▼
[ Current: Streamlit App UI ]                         [ Future: Code Generation Factory ]

Because test outcomes are saved strictly as strongly typed objects, adding downstream execution modules—such as **automatically converting these scenarios into ready-to-run Playwright, Pytest, or Behave automation scripts**—requires zero changes to the core agent logic.

---

## 🛠️ Tech Stack & Prerequisites (100% Free Tier)

* **Core Language:** Python 3.10+
* **LLM Orchestration:** `google-genai` SDK (Gemini 2.5 Flash model via Google AI Studio free tier)
* **Data Validation:** `pydantic`
* **Web Interface:** `streamlit`
* **Configuration:** `python-dotenv`

---

## 💻 Local Installation & Setup

Follow these steps to run the studio environment locally on your machine:

### 1. Clone and Navigate to the Project
```bash
git clone [https://github.com/richaguptaec-cpu/qa-ai-agent-engine.git]
cd qa-ai-agent-engine

python -m venv venv

2. Configure Your Virtual Environment

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux:
source venv/bin/activate

3. Install Dependencies

Bash
pip install google-genai pydantic streamlit python-dotenv

4. Configure Environment Variables
Create a .env file in the root directory:

GEMINI_API_KEY=your_free_google_ai_studio_key_here

5. Launch the Application

streamlit run app.py

The application will open automatically in your browser at http://localhost:8501.

📈 Future Roadmap
[ ] Phase 2 (Automation Translation Factory): Connect an automated source code translator to convert generated Gherkin test matrices into executable pytest-bdd and Playwright automated scripts.

[ ] Phase 3 (Jira / Xray Synchronizer): Integrate Webhook support to dynamically sync generated Acceptance Criteria and Scenarios into enterprise test management solutions.