# 🏗️ JIRAG Platform - Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Dashboard  │  │  Job Search  │  │  AI Agent    │              │
│  │   HTML       │  │  HTML        │  │  HTML        │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                      │
│  ┌──────────────────────────────────────────────────┐              │
│  │         Prediction      │    Notifications      │              │
│  │         HTML            │    HTML               │              │
│  └──────────────────────────────────────────────────┘              │
│         │                                                           │
│  ┌──────────────────────────────────────────────────┐              │
│  │           JavaScript Modules                     │              │
│  │  ├─ app.js (search logic)                        │              │
│  │  ├─ agent.js (chat)                              │              │
│  │  ├─ prediction.js (quiz)                         │              │
│  │  ├─ notifications.js (alerts)                    │              │
│  │  └─ navigation.js (routing)                      │              │
│  └──────────────┬───────────────────────────────────┘              │
│                 │                                                   │
│         Tailwind CSS Styling                                       │
│                 │                                                   │
└─────────────────┼───────────────────────────────────────────────────┘
                  │ HTTP/WebSocket
                  │ JSON
                  │
┌─────────────────▼───────────────────────────────────────────────────┐
│                     API LAYER (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐       │
│  │  Search Routes  │  │ Agent Routes │  │  Prediction     │       │
│  │                 │  │              │  │  Routes         │       │
│  │ • /search/stream│  │ • /agent/*   │  │ • /prediction/* │       │
│  │ • /cv-match     │  │              │  │                 │       │
│  └────────┬────────┘  └──────┬───────┘  └────────┬────────┘       │
│           │                  │                   │                 │
│  ┌────────────────┐  ┌───────────────┐  ┌────────────────┐        │
│  │ Notification   │  │  CORS & Auth  │  │  Request       │        │
│  │ Routes         │  │  Middleware   │  │  Logging       │        │
│  │                │  │               │  │                │        │
│  │ • /notif/*     │  │               │  │                │        │
│  └────────┬───────┘  └───────────────┘  └────────────────┘        │
│           │                                                         │
└───────────┼─────────────────────────────────────────────────────────┘
            │ Pydantic Validation
            │
┌───────────▼───────────────────────────────────────────────────────┐
│              SERVICES LAYER (Business Logic)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ RAG Pipeline     │  │ Career           │                     │
│  │                  │  │ Classifier       │                     │
│  │ • ask_stream()   │  │                  │                     │
│  │ • hybrid_search()│  │ • predict_career │                     │
│  │ • cv_matcher()   │  │ • get_skills()   │                     │
│  └────────┬─────────┘  └────────┬─────────┘                     │
│           │                     │                               │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ Opportunity      │  │ n8n Workflow     │                    │
│  │ Finder           │  │ Manager          │                    │
│  │                  │  │                  │                    │
│  │ • find_opp()     │  │ • send_notif()   │                    │
│  │ • search_*()     │  │ • create_alert() │                    │
│  │ • rank_results() │  │ • manage_flows() │                    │
│  └────────┬─────────┘  └────────┬─────────┘                    │
│           │                     │                              │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ LangGraph        │  │ Source           │                   │
│  │ Agent            │  │ Scrapers         │                   │
│  │                  │  │                  │                   │
│  │ • search_*()     │  │ • linkedin()     │                   │
│  │ • reason()       │  │ • wuzzuf()       │                   │
│  │ • rank()         │  │ • iti()          │                   │
│  │                  │  │ • nti()          │                   │
│  │                  │  │ • facebook()     │                   │
│  └────────┬─────────┘  └────────┬─────────┘                   │
│           │                     │                             │
└───────────┼─────────────────────┼────────────────────────────┘
            │                     │
            │                     │
┌───────────▼─────────────────────▼────────────────────────────┐
│               DATA LAYER                                      │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────┐  ┌────────────────────────┐           │
│  │ Vector Store       │  │ BM25 Index             │           │
│  │ (ChromaDB)         │  │ (Elasticsearch/custom) │           │
│  │                    │  │                        │           │
│  │ • embeddings       │  │ • keyword search       │           │
│  │ • semantic search  │  │ • rank documents       │           │
│  └────────┬───────────┘  └────────┬───────────────┘           │
│           │                       │                           │
│  ┌─────────────────────────────────────────────┐              │
│  │        PostgreSQL Database                  │              │
│  │  ┌──────────────┐  ┌─────────────────┐     │              │
│  │  │ Users Table  │  │ Opportunities   │     │              │
│  │  │ Alerts Table │  │ Predictions     │     │              │
│  │  │ Notif. Logs  │  │ Notifications   │     │              │
│  │  └──────────────┘  └─────────────────┘     │              │
│  └────────┬──────────────────────────┬─────────┘              │
│           │                          │                        │
│  ┌───────────────────┐     ┌──────────────────┐              │
│  │ Job Data (JSON)   │     │ Vector Index     │              │
│  │ • linkedin_full   │     │ (ChromaDB)       │              │
│  │ • wuzzuf_full     │     │ Persistence      │              │
│  └───────────────────┘     └──────────────────┘              │
│                                                                │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│         EXTERNAL SERVICES                                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ Groq LLM         │  │ n8n Workflows    │                   │
│  │                  │  │                  │                   │
│  │ • Analyze text   │  │ • Job Monitor    │                   │
│  │ • Generate text  │  │ • Email Digest   │                   │
│  │ • Explain CV     │  │ • Notification   │                   │
│  │                  │  │   Dispatcher     │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ LinkedIn API     │  │ Wuzzuf API       │                   │
│  │ Scraping Service │  │ Scraping Service │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ ITI/NTI APIs     │  │ Email Service    │                   │
│  │ Course Data      │  │ (SMTP)           │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Job Search Flow
```
User Input
    ↓
Search API (/search/stream)
    ↓
RAG Pipeline
    ├─ Hybrid Search (BM25 + Vector DB)
    ├─ Rank Results
    └─ Score Matches
    ↓
Stream Results (Server-Sent Events)
    ↓
Client Renders Cards
```

### Career Prediction Flow
```
User Completes Quiz
    ↓
Submit Answers → /prediction/quiz
    ↓
Career Classifier
    ├─ Process Responses → Features
    ├─ ML Model Inference
    └─ Score Alternatives
    ↓
Return Prediction + Skills + Paths
    ↓
Client Displays Results
```

### Agent Discovery Flow
```
User Message
    ↓
/agent/search/stream
    ↓
LangGraph Agent
    ├─ Understand Intent
    ├─ Plan Steps
    └─ Execute Multi-Source Search
        ├─ LinkedIn Search
        ├─ Wuzzuf Search
        ├─ ITI/NTI Search
        ├─ Companies Search
        ├─ Facebook Search
        └─ Parallel Execution
    ↓
Rank & Filter Results
    ↓
Generate Reasoning
    ↓
Stream Response (Thinking → Results → Reasoning)
    ↓
Client Displays Chat Message + Cards
```

### Notification Flow
```
Job Alert Created
    ↓
/notifications/job-alert
    ↓
n8n Job Alert Workflow
    ├─ Trigger: Cron (hourly)
    ├─ Search Job Sources
    ├─ Filter by Preferences
    └─ Send Notifications
    ↓
Notification Dispatcher
    ├─ Email
    ├─ Push
    ├─ WhatsApp
    └─ SMS
    ↓
User Receives Alert
    ↓
User Clicks Link
    ↓
Click Logged → Analytics
```

---

## Technology Stack

### Frontend
```
HTML5
├─ Semantic Markup
├─ RTL Support (Arabic)
└─ Accessibility

CSS3 (Tailwind)
├─ Utility-First
├─ Dark Theme
└─ Responsive Grid

JavaScript (ES6+)
├─ Fetch API
├─ Async/Await
├─ Module Pattern
└─ Event Listeners
```

### Backend
```
FastAPI
├─ Async Routes
├─ Pydantic Validation
├─ OpenAPI Documentation
└─ WebSocket Support

Python 3.10+
├─ LangChain
├─ LangGraph
├─ Scikit-learn
├─ ChromaDB
└─ SQLAlchemy
```

### Databases
```
Vector Store
├─ ChromaDB
├─ Embeddings
└─ Semantic Search

Relational DB
├─ PostgreSQL
├─ Users
├─ Alerts
└─ Logs

Search Index
├─ BM25
└─ Keyword Search
```

### External Services
```
AI/LLM
├─ Groq API
└─ OpenAI (optional)

Workflow Automation
├─ n8n
├─ Job Monitoring
├─ Email Delivery
└─ Notifications

Web Scraping
├─ LinkedIn
├─ Wuzzuf
├─ Companies
└─ Social Media
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Docker Containers               │
├─────────────────────────────────────────┤
│                                          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ FastAPI App  │  │ PostgreSQL   │   │
│  │ (port 8000)  │  │ (port 5432)  │   │
│  └──────────────┘  └──────────────┘   │
│                                          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ n8n          │  │ ChromaDB     │   │
│  │ (port 5678)  │  │ (embedded)   │   │
│  └──────────────┘  └──────────────┘   │
│                                          │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ Redis        │  │ Volume Mounts│   │
│  │ (optional)   │  │ (data)       │   │
│  └──────────────┘  └──────────────┘   │
│                                          │
└─────────────────┬──────────────────────┘
                  │
        Docker Compose
                  │
        ┌─────────┴──────────┐
        │                    │
    Docker Hub         Docker Network
        │                    │
    Image Push        Inter-container
                        Networking
```

---

## Performance Considerations

```
Optimization Layers:

1. Client Side
   ├─ Lazy Loading
   ├─ Debouncing
   ├─ Local Caching
   └─ Async Operations

2. API Level
   ├─ Response Compression
   ├─ Pagination
   ├─ Rate Limiting
   └─ Caching Headers

3. Database
   ├─ Indexing
   ├─ Query Optimization
   ├─ Connection Pooling
   └─ Replication

4. Application
   ├─ Async Tasks
   ├─ Batch Operations
   ├─ Parallel Processing
   └─ Result Caching
```

---

## Security Layers

```
1. Network Level
   ├─ HTTPS/TLS
   ├─ Firewall
   └─ DDoS Protection

2. Application Level
   ├─ JWT Authentication
   ├─ CORS Validation
   ├─ Rate Limiting
   └─ Input Sanitization

3. Data Level
   ├─ Encryption at Rest
   ├─ Encryption in Transit
   ├─ Hash Passwords
   └─ Secure API Keys

4. Monitoring
   ├─ Intrusion Detection
   ├─ Log Auditing
   ├─ Error Tracking
   └─ Performance Alerts
```

---

## Scaling Strategy

```
Horizontal Scaling:
├─ Load Balancer
├─ Multiple API Instances
├─ Database Replication
└─ Cache Distribution

Vertical Scaling:
├─ Increase VM Resources
├─ Database Optimization
├─ Connection Pooling
└─ Memory Management

Caching Strategy:
├─ Redis Cache
├─ Browser Cache
├─ CDN for Static Assets
└─ Query Result Cache
```

---

**Last Updated:** April 24, 2026
**Version:** 1.0
