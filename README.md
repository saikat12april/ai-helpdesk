# 🚀 Enterprise AI Support & Helpdesk Platform

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20Llama3-blueviolet?style=for-the-badge" />
</p>

<p align="center">
  <b>AI-Powered Enterprise IT Support, Ticketing & Asset Management System</b>
</p>

---

## 📌 Overview

Enterprise AI Support & Helpdesk Platform is a full-stack AI-powered IT support solution designed to streamline ticket management, automate issue triaging, manage organizational assets, and provide intelligent assistance through Generative AI.

The platform combines:

- 🤖 AI Chat Assistant
- 🎫 Smart Ticket Management
- 👁️ Screenshot Error Analysis
- 🎙️ Voice-Based Interaction
- 📦 Asset Management
- 👥 User & Role Management
- 🔐 Secure Authentication & Authorization

---

## ✨ Key Features

### 🤖 AI Support Assistant

- Real-time conversational support
- Context-aware AI responses
- Powered by Llama 3 & Gemini AI

### 🎫 Smart Ticket System

- Automatic ticket generation
- AI severity prediction
- Status tracking workflow
- Admin & Engineer controls

### 👁️ Vision AI Error Detection

- Upload screenshots of errors
- OCR-based text extraction
- AI-generated troubleshooting steps
- One-click ticket creation

### 🎙️ Voice Assistant

- Speech-to-Text support
- Text-to-Speech responses
- Hands-free ticket creation

### 📦 Asset Management

- Asset inventory tracking
- Assignment management
- Repair & retirement tracking
- Asset lifecycle monitoring

### 👥 User Management

- User registration approval workflow
- Role-based access control
- Employee, Engineer & Admin roles

### 🔐 Enterprise Security

- JWT Authentication
- Password Hashing (Bcrypt)
- Protected API Routes
- Session Persistence

---

# 🏗️ System Architecture

```text
┌──────────────────────────┐
│      Streamlit UI        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       FastAPI API        │
└────────────┬─────────────┘
             │
 ┌───────────┼───────────┐
 ▼           ▼           ▼

MongoDB    Gemini AI    Groq API
 Atlas      Vision       Llama 3
```

---

## 📂 Project Structure

```text
helpdesk_project/
│
├── backend/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── tickets.py
│   │   └── assets.py
│   │
│   ├── models.py
│   ├── database.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── render.yaml
├── .env
└── README.md
```

---

## 🛠️ Tech Stack

| Category        | Technologies       |
| --------------- | ------------------ |
| Frontend        | Streamlit          |
| Backend         | FastAPI            |
| Database        | MongoDB Atlas      |
| AI Models       | Gemini AI, Llama 3 |
| Authentication  | JWT, Passlib       |
| API Server      | Uvicorn            |
| Data Processing | Pandas             |
| Visualization   | Plotly             |

---

## 🔄 Workflow

```text
User
 │
 ▼
Submit Issue
 │
 ▼
AI Analysis
 │
 ▼
Severity Detection
 │
 ▼
Ticket Creation
 │
 ▼
Engineer Assignment
 │
 ▼
Resolution & Closure
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ai-helpdesk.git
cd ai-helpdesk
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_connection_string

GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_gemini_api_key

SECRET_KEY=your_secret_key

API_URL=http://localhost:8000
```

---

## ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

---

## ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

---

## 🌐 Live Deployment

### Frontend

https://ai-helpdesk-frontend-8157.onrender.com

### Backend

https://ai-helpdesk-backend-5jge.onrender.com

---

## 📸 Application Modules

✅ Dashboard

✅ AI Chat Assistant

✅ Voice Support

✅ Screenshot Error Analysis

✅ Ticket Management

✅ Asset Management

✅ User Management

✅ Analytics & Reports

---

## 🚀 Future Enhancements

- Multi-language Support
- Slack / Teams Integration
- Email Ticket Automation
- Predictive Asset Maintenance
- Knowledge Base RAG System
- AI Agent Workflows

---

## 👨‍💻 Developed By

### Saikat Kr De

B.Tech CSE Student

AI • Full Stack Development • Enterprise Automation

---

## 📄 License

Licensed under the MIT License.

See `LICENSE` for more information.
