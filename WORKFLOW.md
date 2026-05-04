# JIRAG - Project Workflow & Technologies Documentation

## Overview

**JIRAG (Jobs RAG Egypt)** is an intelligent career discovery platform for the Egyptian job market. It leverages AI, RAG (Retrieval-Augmented Generation), and automation to help users find jobs, internships, and career opportunities.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (HTML/CSS/JS)                      │
│  Dashboard │ Search │ Agent │ Prediction │ Notifications            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                             │
│  API Routes │ WebSocket Streaming │ Static Files                    │
└─────────────────────────────────────────────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RAG Module    │    │   AI Agents     │    │ Prediction      │
│   Pipeline      │    │   (LangGraph)   │    │ Module          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Hybrid Search   │    │ Multi-Source    │    │ ML Classifier   │
│ BM25 + Vector   │    │ Discovery       │    │ Career Paths    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ChromaDB +      │    │ LinkedIn,       │    │ Skill Gap       │
│ Pinecone        │    │ Wuzzuf, ITI     │    │ Analysis        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     N8N AUTOMATION ENGINE                            │
│  Workflows: Job Alerts │ Email Digests │ WhatsApp Notifications     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Technologies

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async web framework |
| **Pydantic** | Data validation and schema management |
| **Groq API** | LLM inference (Llama 3.1, DeepSeek) |
| **LangGraph** | Multi-agent AI orchestration |

### Data & Search

| Technology | Purpose |
|------------|---------|
| **ChromaDB** | Vector database for embeddings |
| **Pinecone** | Managed vector search (production) |
| **BM25** | Keyword-based retrieval |
| **Hybrid Retriever** | Combines vector + BM25 for best results |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic page structure |
| **Tailwind CSS** | Utility-first styling |
| **Chart.js** | Data visualization |
| **Vanilla JS** | Frontend interactivity |

### Automation

| Technology | Purpose |
|------------|---------|
| **n8n** | Workflow automation |
| **Email** | Job alert notifications |
| **WhatsApp** | Push notifications |

---

## Workflow Description

### 1. Job Search Flow

```
User Query → FastAPI → RAG Pipeline → Hybrid Search → LLM Ranking → Response
                                    │
                                    ▼
                            ┌───────────────┐
                            │ BM25 + Vector │
                            │   Retrieval   │
                            └───────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │  ChromaDB/    │
                            │  Pinecone     │
                            └───────────────┘
```

**Steps:**
1. User enters search query (e.g., "Python developer Cairo")
2. FastAPI receives the request
3. RAG pipeline performs hybrid search (BM25 + vector)
4. Results are filtered for freshness (last 14 days)
5. Groq LLM ranks and explains results
6. Streaming response sent to frontend

### 2. AI Agent Flow

```
User Request → LangGraph Agent → Parallel Source Search → Aggregation → Response
                        │
                        ▼
            ┌───────────────────────┐
            │  Sub-Agents:          │
            │  - LinkedIn Agent     │
            │  - Wuzzuf Agent       │
            │  - ITI/NTI Agent      │
            │  - Company Sites      │
            └───────────────────────┘
```

**Features:**
- Multi-source parallel discovery
- Context-aware recommendations
- Skill matching
- Reasoning explanation

### 3. Career Prediction Flow

```
User Quiz → ML Classifier → Career Recommendation → Skills Gap → Learning Paths
                │
                ▼
        ┌───────────────┐
        │  Scikit-learn │
        │  Classifier  │
        └───────────────┘
```

**Quiz Categories:**
- Technical skills assessment
- Interest mapping
- Experience level
- Career goals

### 4. Notification Flow

```
New Job Alert → n8n Webhook → Workflow Trigger → Multi-channel Push
                            │
                            ▼
                  ┌─────────────────┐
                  │  n8n Workflows  │
                  │  - Job Alerts   │
                  │  - Daily Digest │
                  │  - Weekly Report│
                  └─────────────────┘
```

---

## Data Pipeline

### Job Data Sources

1. **Wuzzuf** - Major Egyptian job portal
2. **LinkedIn** - Professional network jobs
3. **ITI** - Information Technology Institute
4. **NTI** - National Telecommunication Institute
5. **Company Websites** - Direct career pages
6. **Facebook Groups** - Job postings groups

### Data Processing

```
Raw Scraped Data → Cleaning → Embedding → Vector Storage → Search Index
                                          │
                                          ▼
                                   ChromaDB / Pinecone
```

### Freshness Filtering

- Jobs older than 14 days are filtered out
- Status must be "Open"
- Keywords relevance scoring

---

## API Endpoints

### Search
- `POST /search/stream` - Streaming job search
- `POST /search/non-stream` - Non-streaming search

### Agent
- `POST /agent/search` - AI agent search
- `POST /agent/search/stream` - Streaming agent search
- `POST /agent/context` - Set user context
- `GET /agent/sources` - Get available sources

### Prediction
- `POST /prediction/quiz` - Submit quiz, get prediction
- `GET /prediction/skills/{career}` - Get skills for career
- `GET /prediction/paths/{career}` - Get learning paths

### CV Matching
- `POST /cv-match` - Upload CV, get job matches

### Notifications
- `GET /notifications` - Get user notifications
- `POST /notifications/subscribe` - Subscribe to alerts

---

## Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| Dashboard | `/` | Overview stats, charts, quick actions |
| Search | `/search` | Job search with filters |
| AI Agent | `/agent` | Chat with AI agent |
| Prediction | `/prediction` | Career prediction quiz |
| Notifications | `/notifications` | Alert management |

---

## Environment Variables

```
GROQ_API_KEY          # Groq LLM API key
PINECONE_API_KEY      # Pinecone vector DB
PINECONE_ENV          # Pinecone environment
N8N_WEBHOOK_URL       # n8n webhook for notifications
```

---

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn API.main:app --reload --port 8000

# Access the application
# Open: http://localhost:8000
```

---

## Key Files

| File | Purpose |
|------|---------|
| `API/main.py` | FastAPI app entry point |
| `RAG/pipeline.py` | RAG search pipeline |
| `agents/agent_routes.py` | AI agent endpoints |
| `prediction/prediction_routes.py` | Career prediction |
| `database/hybrid_retriever.py` | Hybrid search logic |
| `src/pages/dashboard.html` | Main dashboard UI |

---

## Development Status

- ✅ Job Search (RAG + Hybrid)
- ✅ AI Agent (LangGraph)
- ✅ Career Prediction (ML)
- ✅ CV Matching
- ✅ Notifications (n8n)
- ✅ Dashboard with Charts

---

*Last Updated: May 2026*