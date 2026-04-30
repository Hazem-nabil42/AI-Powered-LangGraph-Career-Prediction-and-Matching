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
                "source": job.get('source', 'unknown')
            })
        
        return {"opportunities": opportunities, "count": len(opportunities)}
    except Exception as e:
        return {"error": str(e), "opportunities": [], "count": 0}

@app.get("/api/dashboard-stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get recent opportunities
        recent = hybrid_search("job opportunities", n_results=50)
        
        total_opportunities = len(recent)
        sources = set()
        for r in recent:
            job = r['job']
            sources.add(job.get('source', 'unknown'))
        
        return {
            "totalOpportunities": total_opportunities,
            "newThisWeek": max(1, int(total_opportunities * 0.2)),
            "applicationsActive": 3,
            "interviewsScheduled": 1,
            "activeSources": len(sources),
            "profileScore": 82,
            "freshJobs": total_opportunities
        }
    except Exception as e:
        return {"error": str(e)}

# CV matching

@app.post("/cv-match")
async def cv_match(file: UploadFile = File(...)):
    # اقرأ الـ PDF
    pdf_bytes = await file.read()

    # جيب الـ matches
    matches, skills_profile = match_cv_to_jobs(pdf_bytes, n_results=5)

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