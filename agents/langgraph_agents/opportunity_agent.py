# agents/langgraph_agents/opportunity_agent.py
"""
Opportunity Agent - Wrapper for multi-source LangGraph RAG pipeline

This module provides a high-level interface to the distributed search graph,
handling initialization, state management, and user context.
"""

from typing import Dict, List, Any, Optional
from .graph import dist_search_app, AgentState
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpportunityAgent:
    """
    Intelligent opportunity finder using LangGraph multi-source routing.
    
    Features:
    - Intelligent source routing (LinkedIn, Facebook, ITI/NTI, Companies)
    - Data freshness filtering (removes >1 month old jobs)
    - Multi-source aggregation with LLM ranking
    - User context awareness for personalized results
    """
    
    def __init__(self):
        """Initialize the opportunity agent with the compiled graph."""
        self.graph = dist_search_app
        self.user_context = {}
        self.sources = {
            "linkedin": {"enabled": True, "priority": 1},
            "companies": {"enabled": True, "priority": 2},
            "iti_nti": {"enabled": True, "priority": 3},
            "facebook": {"enabled": True, "priority": 4},
            "volunteering": {"enabled": True, "priority": 5},
            "learning": {"enabled": True, "priority": 6},
        }
        logger.info("✅ OpportunityAgent initialized with LangGraph")
    
    def set_user_context(self, context: Dict[str, Any]) -> None:
        """
        Set user context for personalized recommendations.
        
        Args:
            context: User profile dict with keys like:
                - skills: List[str]
                - experience_level: str
                - location: str
                - preferred_companies: List[str]
                - preferred_roles: List[str]
        """
        self.user_context = context
        logger.info(f"📋 User context set: {list(context.keys())}")
    
    async def search_opportunities(
        self,
        query: str,
        opportunity_type: str = "all",
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute multi-source search using LangGraph routing.
        
        The search flow:
        1. Router: Analyzes query and selects sources (LinkedIn, Facebook, ITI/NTI, etc.)
        2. Retriever: Searches each source with automatic freshness filtering
        3. Aggregator: Ranks and summarizes results using LLM
        
        Args:
            query: User search query (e.g., "python developer at google")
            opportunity_type: Type filter - 'all', 'jobs', 'internships', 'courses'
            filters: Optional search filters (location, experience level, etc.)
        
        Returns:
            Dict with keys:
                - opportunities: List of matched jobs/programs
                - reasoning: LLM explanation of results
                - sources_used: List of sources that were searched
                - total_results: Count of results found
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🔍 Starting opportunity search: '{query}'")
        logger.info(f"   Type: {opportunity_type} | Filters: {filters}")
        logger.info(f"{'='*60}\n")
        
        # Initialize state with empty defaults
        initial_state: AgentState = {
            "query": query,
            "opportunity_type": opportunity_type,
            "filters": filters or {},
            "user_context": self.user_context,
            "search_sources": [],
            "results": [],
            "final_response": "",
            "sources_used": []
        }
        
        try:
            # Execute the compiled LangGraph
            final_state = self.graph.invoke(initial_state)
            
            # Extract and format results
            opportunities = [
                {
                    "title": r.get("job", {}).get("title", "N/A"),
                    "company": r.get("job", {}).get("company", "N/A"),
                    "location": r.get("job", {}).get("location", "N/A"),
                    "description": r.get("job", {}).get("description", "N/A")[:200],  # Limit to 200 chars
                    "posted_date": r.get("job", {}).get("posted", "N/A"),
                    "experience": r.get("job", {}).get("experience", "N/A"),
                    "salary": r.get("job", {}).get("salary", "Not specified"),
                    "url": r.get("job", {}).get("url", "#"),
                    "source": r.get("job", {}).get("source", "unknown"),
                    "score": r.get("score", 0)
                }
                for r in final_state.get("results", [])
            ]
            
            result = {
                "opportunities": opportunities,
                "reasoning": final_state.get("final_response", ""),
                "sources_used": final_state.get("sources_used", []),
                "total_results": len(opportunities)
            }
            
            logger.info(f"✅ Search complete: {len(opportunities)} opportunities from {len(final_state.get('sources_used', []))} source(s)\n")
            return result
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return {
                "opportunities": [],
                "reasoning": f"Search failed: {str(e)}",
                "sources_used": [],
                "total_results": 0
            }
    
    async def search_by_type(
        self,
        opportunity_type: str,
        query: str = "",
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Specialized search by opportunity type.
        
        Args:
            opportunity_type: 'jobs', 'internships', 'courses', 'volunteering'
            query: Optional search query
            filters: Optional search filters
        
        Returns:
            Search results with type-specific filtering
        """
        typed_query = f"{opportunity_type}: {query}" if query else opportunity_type
        return await self.search_opportunities(typed_query, opportunity_type, filters)
    
    def enable_source(self, source: str) -> None:
        """Enable a data source."""
        if source in self.sources:
            self.sources[source]["enabled"] = True
            logger.info(f"✓ Source '{source}' enabled")
    
    def disable_source(self, source: str) -> None:
        """Disable a data source."""
        if source in self.sources:
            self.sources[source]["enabled"] = False
            logger.info(f"✗ Source '{source}' disabled")
    
    def get_active_sources(self) -> List[str]:
        """Get list of currently active sources."""
        return [s for s, cfg in self.sources.items() if cfg["enabled"]]


# Global agent instance
opportunity_agent = OpportunityAgent()

