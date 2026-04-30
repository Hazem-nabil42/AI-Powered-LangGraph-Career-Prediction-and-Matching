# JIRAG Project Structure & Architecture

## 📁 Project Overview

JIRAG (Jobs/Internships RAG system) is an intelligent career discovery and notification platform built with **FastAPI**, **LangGraph AI**, and **n8n automation**.

### Key Features
- 🔍 **Intelligent Job Search** - Hybrid RAG system with BM25 + Vector DB
- 🤖 **LangGraph AI Agent** - Multi-source opportunity discovery
- 🎯 **Career Prediction** - ML-based career path recommendations  
- 🔔 **n8n Notifications** - Automated smart alerts via email, push, WhatsApp
- 📊 **Dashboard** - Real-time metrics and quick actions
- 🌍 **Multi-Source** - LinkedIn, Wuzzuf, ITI, NTI, Companies, Facebook Groups

---

## 📂 Folder Structure

```
jobs-rag-egypt/
│
├── API/
│   └── main.py                          # FastAPI entry point
│
├── src/                                 # Frontend assets
│   ├── css/
│   │   ├── input.css                   # Tailwind input
│   │   └── output.css                  # Compiled CSS
│   │
│   ├── JS/
│   │   ├── app.js                      # Main app logic
│   │   └── modules/
│   │       ├── agent.js                # AI Agent chat module
│   │       ├── prediction.js           # Career prediction quiz
│   │       ├── notifications.js        # Notification management
│   │       └── navigation.js           # Navigation utilities
│   │
│   └── pages/
│       ├── dashboard.html              # Main dashboard
│       ├── search.html                 # Job search page
│       ├── agent.html                  # AI Agent chat
│       ├── prediction.html             # Career prediction quiz
│       └── notifications.html          # Notification center
│
├── RAG/                                 # Retrieval-Augmented Generation
│   ├── pipeline.py                     # Main RAG pipeline
│   ├── cv_matcher.py                   # CV to job matching
│   └── __init__.py
│
├── agents/                              # LangGraph AI Agent
│   ├── agent_routes.py                 # Agent API endpoints
│   ├── langgraph_agents/
│   │   └── opportunity_agent.py        # Multi-source opportunity finder
│   │
│   └── services/                        # Agent services
│       ├── opportunity_finder.py       # Opportunity aggregation
│       └── scrapers/                   # Data source scrapers
│           ├── linkedin_scraper.py     # LinkedIn integration
│           ├── wuzzuf_scraper.py       # Wuzzuf integration
│           └── __init__.py
│
├── prediction/                          # Career Prediction Module
│   ├── prediction_routes.py            # Prediction API endpoints
│   │
│   └── models/
│       ├── career_classifier.py        # ML classifier
│       │
│       ├── data/                       # Training data
│       │   └── __init__.py
│       │
│       └── __pycache__/
│
├── notification_engine/                 # Notification & n8n Integration
│   ├── notification_routes.py          # Notification API endpoints
│   ├── n8n_integration.py              # n8n API client
│   │
│   └── workflows/                      # n8n workflow definitions
│       ├── workflow_manager.py         # Workflow management
│       ├── job_alert_monitor.json      # Job alert workflow config
│       ├── email_digest.json           # Email digest workflow
│       └── __init__.py
│
├── database/                            # Vector & Search Databases
│   ├── vector_store.py                 # Chroma vector store
│   ├── bm25_index.py                   # BM25 search index
│   ├── hybrid_retriever.py             # Hybrid search
│   ├── search_test.py
│   ├── vector_vs_mg25.py
│   └── chroma_db/                      # ChromaDB storage
│
├── models/                              # Shared Pydantic Models
│   ├── schemas.py                      # Data models
│   └── __init__.py
│
├── scraper/                             # Web scraping utilities
│   ├── base_scraper.py
│   ├── linkedin_scraper.py
│   ├── wuzzuf_scraper.py
│   ├── live_scraper.py
│   │
│   └── details_scraper/                # Detail page scrapers
│       ├── linkedin_details.py
│       ├── wuzzuf_details.py
│       └── check_job_page.py
│
├── data/                                # Data storage
│   ├── raw/
│   │   ├── linkedin_jobs.json
│   │   ├── wuzzuf_jobs.json
│   │   └── *_enriched_temp.json
│   │
│   └── processed/
│       ├── linkedin_full.json
│       └── wuzzuf_full.json
│
├── index.html                           # Landing page
├── tailwind.config.js                   # Tailwind config
├── package.json                         # Node dependencies
├── requirements.txt                     # Python dependencies
├── setup.py                             # Setup script
├── Dockerfile                           # Docker config
├── README.MD                            # Project documentation
└── rag_jobs_system.txt                 # System description
```

---

## 🏗️ Architecture Overview

### Frontend Stack
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first styling
- **Vanilla JavaScript** - ES6+ modules
- **RTL Support** - Arabic language support

### Backend Stack
- **FastAPI** - Modern async Python framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM (when needed)
- **ChromaDB** - Vector embeddings
- **LangGraph** - AI orchestration

### External Integrations
- **n8n** - Workflow automation & notifications
- **Groq** - LLM for analysis
- **LinkedIn** - Job data
- **Wuzzuf** - Job platform
- **ITI/NTI** - Learning opportunities

---

## 🚀 Key Modules

### 1. **RAG Pipeline** (`RAG/`)
- Hybrid search combining BM25 + vector embeddings
- CV matching with job descriptions
- Context-aware job recommendations

**Key Functions:**
- `ask_stream()` - Streaming search results
- `ask_non_stream()` - Standard search
- `hybrid_search()` - Combine multiple search types
- `match_cv_to_jobs()` - CV analysis

### 2. **AI Agent** (`agents/`)
- LangGraph-based multi-step reasoning
- Multi-source opportunity discovery
- Real-time web search integration

**Features:**
- Understands user intent
- Searches across 6+ data sources in parallel
- Ranks results by relevance
- Explains reasoning to user

### 3. **Career Prediction** (`prediction/`)
- 8-question quiz for career assessment
- ML classification (sklearn RandomForest)
- Confidence scoring

**Career Types:**
- Software Development
- Data Science
- UX/UI Design
- Business Analysis
- Product Management
- etc.

### 4. **Notification Engine** (`notification_engine/`)
- Integrates with n8n for automation
- Multi-channel delivery (Email, Push, WhatsApp, SMS)
- Smart scheduling and frequency control

**Workflow Types:**
- Job Alert Monitor (polls sources every 1 hour)
- Email Digest Generator (daily at 9 AM)
- Notification Dispatcher (instant notifications)

---

## 📡 API Endpoints

### Search & Jobs
```
POST   /search/stream           - Stream search results
POST   /cv-match                - Match CV to jobs
```

### Agent
```
POST   /agent/search            - Standard agent search
POST   /agent/search/stream     - Streaming agent search
POST   /agent/context           - Set user context
GET    /agent/sources           - Get available sources
POST   /agent/sources/{id}/toggle - Enable/disable source
```

### Prediction
```
POST   /prediction/quiz         - Submit quiz answers
GET    /prediction/skills/{career} - Get skills for career
GET    /prediction/paths/{career}  - Get learning paths
GET    /prediction/results/{user_id} - Get saved results
POST   /prediction/save/{user_id}   - Save results
```

### Notifications
```
POST   /notifications/send      - Send notification
POST   /notifications/job-alert - Create job alert
POST   /notifications/daily-digest - Create daily digest
POST   /notifications/settings  - Update preferences
GET    /notifications/{user_id}/alerts - Get alerts
```

---

## 🎯 Frontend Pages

### Dashboard (`src/pages/dashboard.html`)
- Welcome message
- Stats cards (profile score, opportunities, applications)
- Quick action cards
- Recent opportunities feed

**JavaScript Module:** `src/JS/modules/navigation.js`

### Job Search (`src/pages/search.html`)
- Real-time search with streaming
- Job cards with match scores
- Source badges (LinkedIn, Wuzzuf)
- Filter options

**JavaScript Module:** `src/JS/app.js`

### AI Agent (`src/pages/agent.html`)
- Chat interface
- Source selection sidebar
- Real-time streaming responses
- Opportunity cards
- Example prompts

**JavaScript Module:** `src/JS/modules/agent.js`

### Career Prediction (`src/pages/prediction.html`)
- 8-question quiz
- Progress indicator
- Results page with:
  - Primary career recommendation
  - Alternative paths
  - Recommended skills
  - Next steps

**JavaScript Module:** `src/JS/modules/prediction.js`

### Notifications (`src/pages/notifications.html`)
- Active alerts tab
- Settings tab (channels, frequency)
- n8n integrations tab
- Workflow status monitoring

**JavaScript Module:** `src/JS/modules/notifications.js`

---

## 🔧 Configuration

### Environment Variables (`.env`)
```
# Groq API
GROQ_API_KEY=your_api_key_here

# n8n Configuration
N8N_API_KEY=your_n8n_key
N8N_BASE_URL=http://localhost:5678

# Database
DATABASE_URL=postgresql://user:pass@localhost/jirag

# Vector DB
CHROMA_COLLECTION=jirag_jobs
```

### Tailwind Config
`tailwind.config.js` - Configured for dark theme with teal accents

---

## 🚀 Running the Project

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install
```

### Development
```bash
# Start FastAPI server
python -m uvicorn API.main:app --reload --host 127.0.0.1 --port 8000

# Serve frontend (if needed)
# Open http://localhost:8000
```

### Production
```bash
# Docker
docker build -t jirag .
docker run -p 8000:8000 jirag

# Or use uvicorn with gunicorn
gunicorn API.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 📊 Data Models

All Pydantic models in `models/schemas.py`:

- **Opportunity** - Job/internship/learning data
- **User** - User profile
- **JobAlert** - Alert configuration
- **CareerPredictionResult** - Prediction output
- **NotificationPreferences** - User preferences
- **Notification** - Sent notification data

---

## 🔐 Security Considerations

- [ ] API authentication (JWT tokens)
- [ ] Rate limiting
- [ ] CORS validation
- [ ] Input sanitization
- [ ] SQL injection protection
- [ ] API key encryption

---

## 📈 Future Enhancements

- [ ] User accounts & authentication
- [ ] Database persistence
- [ ] Advanced analytics
- [ ] Mobile app (React Native)
- [ ] More data sources
- [ ] Collaborative features
- [ ] Machine learning model improvements
- [ ] Real-time bidding system

---

## 📝 Notes

- Frontend uses RTL (Right-to-Left) for Arabic support
- All timestamps in UTC
- Responsive design (mobile-first)
- No external UI library dependencies (pure Tailwind)

---

Last Updated: April 2026
