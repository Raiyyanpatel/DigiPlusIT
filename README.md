# 🤖 ResolveAI

An AI-powered, multi-agent IT Service Desk built for fully autonomous triage, root cause analysis, and resolution.

ResolveAI uses LangGraph to orchestrate multiple specialized agents powered by Gemini. It processes incoming incidents, searches a vectorized knowledge base (RAG) and historical incidents, diagnoses the root cause, and takes action across external tools (GitHub, Asana, Slack).

## 🌟 Features
- **Multi-Agent Architecture**: Built with LangGraph, delegating tasks between Triage, Knowledge, Investigation, and Action agents.
- **RAG & Embeddings**: Uses `gemini-embedding-2` to vectorize internal knowledge base documents and historical tickets via pgvector.
- **Automated External Actions**: Connects to GitHub to create issues, Asana to create tasks, and Slack for alerts.
- **Copilot Chat**: Features an interactive AI side-panel on the frontend for engineers to brainstorm and resolve incidents manually with the AI's assistance.
- **Observability**: Built-in Prometheus metrics and Redis caching.

## 🏗️ Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for a deep dive into the LangGraph flow, tech stack, and agent responsibilities.

---

## 🚀 Getting Started

### 1. Prerequisites
- [Docker & Docker Compose](https://www.docker.com/)
- API Keys for Gemini, Asana (optional), GitHub (optional), and a Slack Webhook (optional).

### 2. Configuration
Clone the repository and set up your environment variables:
```bash
# Copy the example environment file
cp .env.example .env
```
Open `.env` and fill in the required `GEMINI_API_KEY`. If you want to use the external tools, add your GitHub Token, Asana PAT, and Slack Webhook URL.

### 3. Running the Stack
Use Docker Compose to spin up the entire application:
```bash
docker compose up -d --build
```
This single command spins up:
- **Postgres** (with pgvector for embeddings)
- **Redis** (for caching)
- **FastAPI Backend** (Port 8000)
- **React/Vite Frontend** (Port 3000)
- **Prometheus** (Port 9090)

### 4. Usage
- **Frontend Dashboard**: Open `http://localhost:3000` in your browser.
- **API Docs**: Open `http://localhost:8000/docs` to interact with the FastAPI Swagger UI.

---

## 👥 Default Accounts
When you run `docker compose up`, the backend will automatically run database migrations and seed the initial RAG knowledge base. The following local accounts are created:
- **Admin**: `admin@resolveai.internal` / `admin123`
- **Engineer**: `engineer@resolveai.internal` / `engineer123`
