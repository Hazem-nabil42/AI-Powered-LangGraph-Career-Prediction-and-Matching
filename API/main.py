# API/main.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pathlib  # Import the whole module to avoid naming conflicts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from RAG.pipeline import ask_stream, ask_non_stream, hybrid_search
# CV mathcer
from fastapi import UploadFile, File
from RAG.cv_matcher import match_cv_to_jobs
from groq import Groq
from dotenv import load_dotenv
import json

# Import new routers
from prediction.prediction_routes import router as prediction_router
from agents.agent_routes import router as agent_router
from notification_engine.notification_routes import router as notification_router

#n8n requests
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Groq for cv reading
groq_client = Groq(api_key=GROQ_API_KEY)

# init faskapi server
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files ──
app.mount("/src", StaticFiles(directory="src"), name="src")

# Include routers
app.include_router(prediction_router)
app.include_router(agent_router)
app.include_router(notification_router)


class SearchRequest(BaseModel):
    query: str

# streaming

@app.post("/search/stream")
async def search_stream(req: SearchRequest):
    return StreamingResponse(
        ask_stream(req.query),
        media_type="text/event-stream"
    )

@app.get("/api/recent-opportunities")
async def get_recent_opportunities(limit: int = 8):
    """Get recently posted job opportunities (fresh ones only)"""
    try:
        # Search for general terms to get fresh opportunities
        results = hybrid_search("new job opportunities fresh", n_results=limit)
        
        opportunities = []
        for r in results:
            job = r['job']
            opportunities.append({
                "title": job.get('title', 'N/A'),
                "company": job.get('company', 'N/A'),
                "location": job.get('location', 'N/A'),
                "experience": job.get('experience', 'N/A'),
                "level": job.get('level', 'N/A'),
                "job_type": job.get('job_type', 'N/A'),
                "posted": job.get('posted', 'Recently'),
                "url": job.get('url', '#'),
                "source": job.get('source', 'wuzzuf'),
                "match": int(r.get('score', 0) * 100) if r.get('score') else 85
            })
        
        return {"opportunities": opportunities, "count": len(opportunities)}
    except Exception as e:
        return {"error": str(e), "opportunities": [], "count": 0}

@app.get("/api/dashboard-stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get recent opportunities to aggregate stats
        recent = hybrid_search("job opportunities technical developers engineers", n_results=50)
        
        total_opportunities = len(recent)
        sources = set()
        source_counts = {}
        for r in recent:
            job = r['job']
            src = job.get('source', 'wuzzuf')
            sources.add(src)
            source_counts[src] = source_counts.get(src, 0) + 1
            
        # Mock some profile strength stats for the dashboard demo, but realistic job counts
        return {
            "totalOpportunities": total_opportunities,
            "newThisWeek": max(1, int(total_opportunities * 0.4)), # estimate
            "applicationsActive": 5,
            "interviewsScheduled": 1,
            "activeSources": len(sources),
            "profileScore": 82,
            "freshJobs": total_opportunities,
            "sourceDistribution": [{"label": k, "value": v} for k, v in source_counts.items()]
        }
    except Exception as e:
        return {"error": str(e)}

# CV matching

@app.post("/cv-match")
async def cv_match(file: UploadFile = File(...)):
    # اقرأ الـ PDF
    pdf_bytes = await file.read()

    # جيب الـ matches
    matches, skills_profile = await match_cv_to_jobs(pdf_bytes, n_results=5)

    if not matches:
        return {"error": "مش قادر أقرأ الـ CV"}

    # اسأل الـ LLM يشرح النتايج
    jobs_text = "\n".join([
        f"- {m['title']} @ {m['company']} ({m['match']}% match)"
        for m in matches
    ])

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""بناءً على الـ CV، دي أنسب الوظايف:
            {jobs_text}

            اشرح بالعربي ليه الوظايف دي مناسبة في 3 جمل بس."""
        }],
        max_tokens=300
    )

    return {
        "matches": matches,
        "summary": response.choices[0].message.content
    }



# non-streaming (for testing/debugging)

@app.post("/search/non-stream")
async def search_non_stream(req: SearchRequest):
    # Use the non-streaming version
    answer, jobs = await ask_non_stream(req.query)
    
    # Debug - شوف إيه اللي بيترجع
    print(f"Jobs found: {len(jobs)}")
    print(f"First job: {jobs[0] if jobs else 'NONE'}")
    
    return {"answer": answer, "jobs": jobs}

# ── Page Routes ──
@app.get("/")
async def root():
    return FileResponse("src/pages/dashboard.html")

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("src/pages/dashboard.html")

@app.get("/search")
async def search_page():
    return FileResponse("src/pages/search.html")

@app.get("/agent")
async def agent_page():
    return FileResponse("src/pages/agent.html")

@app.get("/prediction")
async def prediction_page():
    return FileResponse("src/pages/prediction.html")

@app.get("/notifications")
async def notifications_page():
    return FileResponse("src/pages/notifications.html")


# n8n 

def trigger_n8n_webhook(job_details):
    # ده الـ Test URL اللي انت أخدته من n8n
    webhook_url = "http://localhost:5678/webhook-test/job-alert"
    
    # تفاصيل الوظيفة اللي هتبعتها للواتساب أو التليجرام
    payload = {
        "title": job_details.get("title", "Unknown Job"),
        "company": job_details.get("company", "Unknown Company"),
        "url": job_details.get("url", "https://linkedin.com")
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("✅ Webhook triggered successfully!")
        else:
            print(f"❌ Failed to push to n8n {response.text}")
    except Exception as e:
        print(f"❌ Connection error to n8n: {e}")


@app.get("/api/test-n8n")
def test_n8n_integration():
    test_job = {
        "title": "Senior Python Developer",
        "company": "Tech Valley",
        "url": "https://wuzzuf.net/jobs/123"
    }
    trigger_n8n_webhook(test_job)
    return {"status": "Test sent to n8n!"}