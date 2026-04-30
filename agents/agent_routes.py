# agents/agent_routes.py
"""
API routes for AI Agent
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
from agents.langgraph_agents.opportunity_agent import opportunity_agent
import json

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQuery(BaseModel):
    """User query to the agent"""
    query: str
    opportunity_type: str = "all"
    filters: Optional[Dict] = None
    user_context: Optional[Dict] = None


class AgentResponse(BaseModel):
    """Agent response"""
    query: str
    response: str
    opportunities: List[Dict]
    sources_used: List[str]
    reasoning: str


@router.post("/search")
async def agent_search(data: AgentQuery) -> AgentResponse:
    """
    Search for opportunities using intelligent agent
    
    Args:
        data: Agent search query
        
    Returns:
        Opportunities and AI explanation
    """
    try:
        # Set user context if provided
        if data.user_context:
            opportunity_agent.set_user_context(data.user_context)
        
        # Execute agent search
        results = await opportunity_agent.search_opportunities(
            query=data.query,
            opportunity_type=data.opportunity_type,
            filters=data.filters
        )
        
        return AgentResponse(
            query=data.query,
            response=results["reasoning"],
            opportunities=results["opportunities"],
            sources_used=results["sources_used"],
            reasoning=results["reasoning"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/stream")
async def agent_search_stream(data: AgentQuery):
    """
    Stream agent search results
    Streams opportunities and reasoning as they're found
    """
    async def event_generator():
        try:
            # Set user context
            if data.user_context:
                opportunity_agent.set_user_context(data.user_context)
            
            # Execute search with streaming
            results = await opportunity_agent.search_opportunities(
                query=data.query,
                opportunity_type=data.opportunity_type,
                filters=data.filters
            )
            
            # Stream opportunities
            yield f"data: {json.dumps({'type': 'thinking', 'content': 'Searching across multiple sources...'})}\n\n"
            
            # Stream each opportunity
            for opp in results["opportunities"]:
                yield f"data: {json.dumps({'type': 'opportunity', 'data': opp})}\n\n"
            
            # Stream reasoning
            yield f"data: {json.dumps({'type': 'reasoning', 'content': results['reasoning']})}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/context")
async def set_context(data: Dict):
    """
    Set user context for better recommendations
    
    Can include: skills, experience, preferences, career goals, etc.
    """
    try:
        opportunity_agent.set_user_context(data)
        return {"status": "success", "message": "Context updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources")
async def get_sources():
    """Get available data sources and their status"""
    return {
        "sources": opportunity_agent.sources,
        "total": len(opportunity_agent.sources),
        "enabled": sum(1 for s in opportunity_agent.sources.values() if s["enabled"])
    }


@router.post("/sources/{source}/toggle")
async def toggle_source(source: str, enabled: bool):
    """Enable or disable a data source"""
    try:
        if enabled:
            opportunity_agent.enable_source(source)
        else:
            opportunity_agent.disable_source(source)
        
        return {"status": "success", "source": source, "enabled": enabled}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
