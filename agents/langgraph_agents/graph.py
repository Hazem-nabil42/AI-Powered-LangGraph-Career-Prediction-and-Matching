from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# State Definition
class AgentState(TypedDict):
    query: str
    opportunity_type: str
    filters: Optional[Dict]
    user_context: Optional[Dict]
    search_sources: List[str]
    results: List[Dict[str, Any]]
    final_response: str
    sources_used: List[str]

# 1. Router Node: decides which sources to query
def router_node(state: AgentState) -> AgentState:
    """
    LLM-based router that analyzes the query and determines relevant sources.
    Uses Groq LLM to intelligently route queries to appropriate data sources.
    """
    query = state["query"]
    print(f"🧭 Routing query: '{query}'")
    
    prompt = f"""
Given the user query: "{query}", decide which data sources are most relevant to search.
Possible sources: linkedin, companies, iti_nti, facebook, volunteering, learning.

Rules:
- For general software/internship/job roles without a specific non-linkedin platform mentioned, choose 'linkedin'.
- If the user explicitly mentions facebook or facebook groups, choose 'facebook'.
- If the user explicitly mentions ITI, NTI, courses, academies, choose 'iti_nti'.
- If the user mentions working at a specific company officially or requests their official website, choose 'companies'.
- If the user mentions volunteering, choose 'volunteering'.
- If the user mentions learning, courses, or training, choose 'learning'.

Output ONLY a comma-separated list of EXACT source names. Default to 'linkedin' if unsure.
Example output: linkedin,iti_nti
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a routing agent. Output ONLY the comma-separated source names."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3
        )
        sources_str = response.choices[0].message.content.lower().strip()
        
        # Parse the response
        selected_sources = []
        for s in ["linkedin", "companies", "iti_nti", "facebook", "volunteering", "learning"]:
            if s in sources_str:
                selected_sources.append(s)
        
        if not selected_sources:
            selected_sources = ["linkedin"]  # fallback
        
        state["search_sources"] = selected_sources
        print(f"  ✓ Routing to sources: {', '.join(selected_sources)}")
        return state
    except Exception as e:
        print(f"⚠️  Router error: {e}, defaulting to linkedin")
        state["search_sources"] = ["linkedin"]
        return state


# 2. Retrieval Functions (synchronous)
def search_linkedin(query: str, n_results=5) -> List[Dict]:
    """
    Search LinkedIn jobs using Pinecone vector DB with hybrid search.
    Includes automatic freshness filtering.
    """
    try:
        from database.pinecone_retriever import hybrid_search
        results = hybrid_search(query, n_results=n_results)
        print(f"  📊 LinkedIn: Found {len(results)} fresh jobs")
        return results
    except Exception as e:
        print(f"  ⚠️  LinkedIn search error: {e}")
        return []


def search_facebook(query: str) -> List[Dict]:
    """
    Search Facebook groups for job posts.
    Currently mocked - ready for integration with actual Facebook API/scraper.
    """
    print(f"  📘 Facebook: Searching groups...")
    # TODO: Replace with actual Facebook API or scraper
    return [{
        "job": {
            "title": f"Facebook Job: {query[:25]}...",
            "company": "Facebook Group: Jobs in Egypt",
            "location": "Remote / Cairo",
            "description": "Job post from Facebook group - [Mock Data]",
            "url": "https://facebook.com/groups/jobsegypt",
            "source": "facebook"
        },
        "score": 0.90
    }]


def search_iti_nti(query: str) -> List[Dict]:
    """
    Search ITI/NTI official websites for programs and opportunities.
    Currently mocked - ready for integration with web scrapers.
    """
    print(f"  🎓 ITI/NTI: Searching programs...")
    # TODO: Replace with actual ITI/NTI website scrapers
    return [{
        "job": {
            "title": f"ITI/NTI Program: {query[:25]}...",
            "company": "Information Technology Institute (ITI)",
            "location": "Smart Village, Cairo",
            "description": "Professional training program - [Mock Data]",
            "url": "https://iti.gov.eg",
            "source": "iti_nti"
        },
        "score": 0.90
    }]


def search_companies(query: str) -> List[Dict]:
    """
    Search company career pages and official job listings.
    Currently mocked - ready for integration with company-specific scrapers.
    """
    print(f"  🏢 Companies: Searching career pages...")
    # TODO: Replace with actual company careers scraper
    return [{
        "job": {
            "title": f"Company Job: {query[:25]}...",
            "company": "Direct Company Portal",
            "location": "Cairo, Egypt",
            "description": "Job opening from company careers page - [Mock Data]",
            "url": "https://company-careers.example.com",
            "source": "companies"
        },
        "score": 0.90
    }]


# 3. Retriever Node
def retriever_node(state: AgentState) -> AgentState:
    """
    Executes searches across all selected sources.
    Aggregates results from multiple sources.
    """
    query = state["query"]
    sources = state["search_sources"]
    all_results = []
    used_sources = []
    
    print(f"\n🔍 Searching {len(sources)} source(s)...")
    
    # Execute searches based on selected sources
    if "linkedin" in sources:
        results = search_linkedin(query, n_results=5)
        all_results.extend(results)
        used_sources.append("linkedin")
    
    if "facebook" in sources:
        results = search_facebook(query)
        all_results.extend(results)
        used_sources.append("facebook")
    
    if "iti_nti" in sources:
        results = search_iti_nti(query)
        all_results.extend(results)
        used_sources.append("iti_nti")
    
    if "companies" in sources:
        results = search_companies(query)
        all_results.extend(results)
        used_sources.append("companies")
    
    if "volunteering" in sources:
        print(f"  🤝 Volunteering: [Mock search]")
        used_sources.append("volunteering")
    
    if "learning" in sources:
        print(f"  📚 Learning: [Mock search]")
        used_sources.append("learning")
    
    state["results"] = all_results
    state["sources_used"] = used_sources
    print(f"  ✓ Total results from {len(used_sources)} source(s): {len(all_results)} opportunities\n")
    return state


# 4. Aggregator/Ranker Node
def aggregator_node(state: AgentState) -> AgentState:
    """
    Formats and explains the search results using LLM.
    Generates a comprehensive summary of why results match the user query.
    """
    query = state["query"]
    results = state.get("results", [])
    
    if not results:
        state["final_response"] = "لم أستطع العثور على أي فرص مناسبة. حاول تعديل بحثك أو المحاولة لاحقاً."
        return state
    
    print(f"📝 Formatting {len(results)} results...")
    
    # Format results for LLM context
    text_context = "Opportunities found:\n\n"
    for i, r in enumerate(results[:10], 1):
        job = r.get('job', {})
        source = job.get('source', 'unknown')
        text_context += f"{i}. {job.get('title', 'N/A')}\n"
        text_context += f"   Company: {job.get('company', 'N/A')}\n"
        text_context += f"   Location: {job.get('location', 'N/A')}\n"
        text_context += f"   Source: {source}\n"
        text_context += f"   URL: {job.get('url', 'N/A')}\n\n"
    
    prompt = f"""You are an intelligent career opportunity recommendation agent.

User Query: "{query}"

Here are opportunities found across multiple sources:
{text_context}

Write a brief, encouraging summary (in Arabic) explaining why these opportunities match the user's request.
Focus on relevance and potential. Be concise (2-3 sentences max).
Do NOT list the opportunities yourself - just explain the relevance."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful career advisor speaking Arabic."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        state["final_response"] = response.choices[0].message.content
        print(f"✓ Aggregation complete")
        return state
    except Exception as e:
        print(f"⚠️  Aggregator error: {e}")
        state["final_response"] = f"تم العثور على {len(results)} فرصة متعلقة بـ: {query}\nتفاصيل الفرص موضحة أعلاه."
        return state


# ═══════════════════════════════════════════════════════════════
# 5. Build and Compile the LangGraph
# ═══════════════════════════════════════════════════════════════
def build_graph():
    """
    Constructs the LangGraph state machine.
    
    Flow:
    START → Router → Retriever → Aggregator → END
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("aggregator", aggregator_node)
    
    # Define flow
    workflow.add_edge(START, "router")
    workflow.add_edge("router", "retriever")
    workflow.add_edge("retriever", "aggregator")
    workflow.add_edge("aggregator", END)
    
    return workflow.compile()


# Compile the graph at module load time
dist_search_app = build_graph()

