# Enterprise AI Support & Helpdesk Platform

A multi-modal, role-based IT helpdesk platform engineered to automate ticket triaging, resolve routine requests through GenAI text/voice streams, and consolidate asset workflows.

## 🚀 Key Features

- **Multi-Modal Support:** AI Assistant equipped for text, screen artifacts, and browser-native voice streaming.
- **Vision AI Triage:** Screenshot Error Analyzer converting visual error captures directly into structural support tickets.
- **Automatic Priority Routing:** Context-aware LLM text analysis parsing incoming requests into structural risk tiers.
- **Role-Based Workflows:** Distinct operational interfaces built for Administrators, IT Engineers, and Employees.
- **Unified Inventory Console:** Full database CRUD interface managing corporate hardware assets and software nodes.

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly, HTML5/CSS3 Custom Animations
- **Backend:** FastAPI, Uvicorn, Pydantic v2
- **Database:** MongoDB Atlas, MongoEngine Object-Data Mapper
- **Core Orchestration:** Groq API (Llama 3), Google Gemini Vision API

## 📂 Project Structure

```text
helpdesk_project/
├── backend/
│   ├── routes/
│   │   ├── assets.py
│   │   ├── auth.py
│   │   └── tickets.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── frontend/
│   └── app.py
├── .gitignore
├── LICENSE
├── render.yaml
└── requirements.txt
```
