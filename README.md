# ResolveAI: Autonomous IT Support Platform

ResolveAI is a cutting-edge, AI-driven IT Service Management (ITSM) platform designed to automatically triage, investigate, and resolve support tickets. Leveraging the power of LangGraph and OpenAI's GPT-4o-mini, ResolveAI acts as an autonomous agent that can connect to your infrastructure, diagnose issues, and interact with third-party tools like Asana and GitHub.

---

## 🏗️ In-Depth Architecture: Multi-Agent System

ResolveAI's core intelligence is driven by an autonomous multi-agent workflow orchestrated using **LangGraph**. Instead of relying on a single monolithic LLM prompt to solve IT issues, the system distributes cognitive load across specialized agent nodes. Each agent operates with specific system prompts, tools, and constraints, interacting through a shared graph state.

### The LangGraph State Machine

The entire lifecycle of an incident is modeled as a Directed Acyclic Graph (DAG) state machine.

```mermaid
graph TD
    Start[Incident Triggered] --> Triage(Triage Agent)
    
    Triage -->|Priority P1/P2| Investigate(Investigation Agent)
    Triage -->|Priority P3/P4| Investigate
    Triage -->|Spam/Invalid| End(End State)
    
    Investigate -->|Needs Human API Action| Action(Action Agent)
    Investigate -->|Self-Resolved| End
    
    Action --> GithubTool{GitHub Tool}
    Action --> AsanaTool{Asana Tool}
    Action --> SlackTool{Slack Tool}
    
    GithubTool --> Validate(Validate Action)
    AsanaTool --> Validate
    SlackTool --> Validate
    
    Validate --> End
```

### 1. Triage Agent (The Router)
- **Role**: Acts as the entry point and semantic router.
- **Cognitive Process**: Reads the raw incident text, analyzes historical context, and infers user urgency.
- **Responsibilities**:
  - Assigns severity/priority (P1 - Critical, P2 - High, P3 - Medium, P4 - Low).
  - Determines categorizations (Network, Database, Access Control, etc.).
  - Decides whether the incident is actionable or spam.
  - Updates the shared `AgentState` with this metadata and passes control.

### 2. Investigation Agent (The Diagnostic Brain)
- **Role**: Investigates the incident deeply.
- **Cognitive Process**: Uses Chain-of-Thought (CoT) reasoning to break down the symptom into potential root causes.
- **Tool Access**: Has read-only access to vector databases, knowledge bases, and log search tools (e.g., querying Splunk or Elasticsearch APIs in an enterprise setting).
- **Responsibilities**:
  - Identifies the most likely root cause.
  - Drafts a step-by-step remediation plan.
  - Decides if the issue can be resolved with a known automated runbook or if it requires human escalation.

### 3. Action Agent (The Executor)
- **Role**: Connects the AI's decisions to the physical world via side effects.
- **Cognitive Process**: Evaluates the remediation plan drafted by the Investigation Agent and selects the appropriate external API tools.
- **Tool Access**: Full write access via strictly typed function calling (OpenAI native function calling).
- **Integrations**:
  - **GitHub API**: Automatically creates bug reports or engineering escalation tickets, carrying over all diagnostic logs.
  - **Asana API**: Creates task items in specific IT project boards and assigns them to on-call technicians.
  - **Slack API**: Fires webhook alerts into `#incident-management` channels for P1/P2 critical issues.

### State Management & Safeguards
- **Shared Memory**: The `AgentState` object is passed between nodes, maintaining an immutable append-only log of what every agent thought and did.
- **Human-in-the-Loop (HITL)**: LangGraph can be paused at the Action Agent stage to require human approval before mutating external state (e.g., before rebooting a server).
- **Rate Limiting Guardrails**: Designed carefully to respect API rate limits, especially for free-tier LLM models.

---

### System Components
- **Frontend (React + Vite)**: A stunning, responsive UI built with Tailwind CSS. Features real-time dashboards, an AI Copilot chat interface, and detailed incident timelines.
- **Backend (FastAPI)**: A high-performance Python API that orchestrates the AI agents and manages the Postgres database interactions.
- **Database (PostgreSQL)**: The primary relational store for incidents, users, and audit logs.
- **Cache / Message Broker (Redis)**: Handles rate limiting, session caching, and async task queues for the AI agents.
- **Infrastructure (Docker)**: Everything is containerized and orchestrated via Docker Compose for seamless local development and deployment.

---

## 🛠️ Technology Stack

**Frontend**
- React 18
- Vite
- Tailwind CSS
- Lucide React (Icons)
- React Router DOM

**Backend**
- Python 3.12
- FastAPI
- LangGraph (Agentic Orchestration)
- Langchain OpenAI
- SQLAlchemy (ORM)
- Pydantic (Data Validation)

**Data & DevOps**
- PostgreSQL
- Redis
- Docker & Docker Compose
- Prometheus & Grafana (Monitoring)

**Integrations**
- OpenAI GPT-4o-mini (`gpt-4o-mini`)
- Asana API
- GitHub API
- Slack Webhooks

---

## 🚀 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- An OpenAI API Key (get one at [platform.openai.com](https://platform.openai.com/api-keys)).
- (Optional) Asana Personal Access Token and GitHub Fine-grained Token if you want the agent to create real tickets.

### 1. Environment Configuration

Create a `.env` file in the root directory. You can copy the example below:

```bash
# .env

# ==========================================
# Application Settings
# ==========================================
APP_ENV=development
POSTGRES_USER=resolveai
POSTGRES_PASSWORD=resolveai_secret
POSTGRES_DB=resolveai
DATABASE_URL=postgresql://resolveai:resolveai_secret@postgres:5432/resolveai
REDIS_URL=redis://redis:6379/0

# ==========================================
# AI Model Configuration (OpenAI)
# ==========================================
# We use gpt-4o-mini for high speed and cost efficiency
OPENAI_API_KEY=your_openai_api_key_here

# ==========================================
# External Integrations
# ==========================================
# ASANA
ASANA_ACCESS_TOKEN=your_asana_pat_here
ASANA_WORKSPACE_ID=your_workspace_id
ASANA_PROJECT_ID=your_project_id

# GITHUB
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your_org/your_repo

# SLACK
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 2. Running the Application

ResolveAI uses Docker Compose to spin up the entire stack (Frontend, Backend, Database, and Cache) with a single command.

Open your terminal in the root directory and run:

```bash
docker compose up -d --build
```

### 3. Accessing the Services

Once the containers are running, you can access the services at the following URLs:

- **Frontend UI**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)

---

## 🧠 How the AI Agents Work

When a new incident is created via the dashboard (or API):
1. A `POST /api/v1/ai/{incident_id}/analyze` request is triggered.
2. The **LangGraph** workflow initializes.
3. The **Triage Agent** assigns a severity (e.g., P2).
4. Control passes to the **Investigation Agent**, which formulates a root cause (e.g., "VPN Certificate Expired").
5. The **Action Agent** receives the diagnosis and decides what to do next. If it determines a ticket needs to be escalated to engineering, it will utilize the `github.py` tool to create a GitHub issue, or the `asana.py` tool to assign a task to the IT team.
6. The resulting JSON payload is returned to the frontend and visualized in the **AI Resolution Report** and **Activity Timeline**.

---

## 🛑 Troubleshooting

**Changes in Frontend aren't showing up?**
Because Vite runs inside a Docker container, sometimes local file changes aren't synced properly depending on your OS. To force a hard rebuild of the frontend:
```bash
docker compose up -d --build frontend
```

**Rate Limit or Auth Errors from OpenAI?**
Ensure your `OPENAI_API_KEY` in `.env` is valid. The platform uses `gpt-4o-mini` which has generous rate limits, but if you are on a free-tier OpenAI account you may need to add billing. Check your usage at [platform.openai.com/usage](https://platform.openai.com/usage).

**Integrations Failing?**
Double-check your `ASANA_PROJECT_ID` and ensure your `GITHUB_TOKEN` has `issues:write` permissions. The tools are hardcoded to read from the environment variables to prevent AI hallucinations.
