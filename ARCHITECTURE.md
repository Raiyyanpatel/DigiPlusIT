# 🏛️ ResolveAI Architecture

ResolveAI leverages a modern AI-centric architecture, separating concerns between API delivery, persistent storage, vector retrieval, and orchestrated LLM agent execution.

## ⚙️ Tech Stack
- **Backend Framework**: FastAPI (Python 3.12)
- **Frontend**: React + Vite + TailwindCSS
- **Database**: PostgreSQL with `pgvector` extension for embeddings
- **Caching & Rate Limiting**: Redis & SlowAPI
- **AI/LLM**: Google Gemini (`gemini-1.5-flash`), `langchain-google-genai`
- **Orchestration**: LangGraph
- **Infrastructure**: Docker & Docker Compose

## 🧠 LangGraph Multi-Agent Workflow

The core of ResolveAI is the autonomous resolution workflow, represented as a state graph using `LangGraph`.

When a new incident is created, it enters the graph and passes through specialized agents:

1. **Triage Agent**
   - **Responsibility**: Analyzes the raw incident text.
   - **Action**: Extracts the category (e.g., Network, Database, Security) and assigns an initial priority (Low, Medium, High, Critical).

2. **Knowledge Agent**
   - **Responsibility**: Gathers context to help solve the issue.
   - **Action**: Queries the PostgreSQL `pgvector` database for similar historical incidents and relevant internal Knowledge Base articles using `gemini-embedding-2`. 

3. **Investigation Agent**
   - **Responsibility**: Synthesizes the incident details and the retrieved RAG context.
   - **Action**: Diagnoses the probable root cause, proposes a step-by-step resolution plan, and dictates which external actions (if any) need to be taken.

4. **Action Agent**
   - **Responsibility**: Executes external integrations based on the Investigation Agent's recommendations.
   - **Tools**:
     - `create_github_issue`: Creates a bug ticket in a designated GitHub repo.
     - `create_asana_task`: Creates an actionable task in an Asana project.
     - `send_slack_notification`: Pings a Slack channel via webhook for high-priority alerts.

Once the Action Agent concludes, the incident is updated with the AI's full analysis, timeline of steps, and recommended next actions. An engineer can then review the incident on the frontend and chat with the **AI Copilot** (context-aware of the incident) to manually resolve it.

## 🗄️ Database Schema (pgvector)
The database stores standard relational data alongside high-dimensional vector embeddings:
- **Incidents**: Tracks the lifecycle, status, and AI analysis.
- **Incident Embeddings**: Stores the 3072-dimensional embedding of the incident text to find similar tickets later.
- **Knowledge Base**: Markdown documents chunked and embedded for RAG retrieval.
- **Resolutions**: Stored when an incident is closed, contributing to the historical dataset.
