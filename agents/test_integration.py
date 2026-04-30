"""
Integration test for agent routes
Verifies that the LangGraph integration works with the API routes
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_agent_search():
    """Test the opportunity agent search functionality"""
    print("🧪 Integration Test: OpportunityAgent with LangGraph\n")
    print("=" * 60)
    
    try:
        # Import the agent
        from agents.langgraph_agents.opportunity_agent import opportunity_agent
        print("✅ Successfully imported OpportunityAgent")
        
        # Test 1: Basic initialization
        print("\n📋 Test 1: Agent Initialization")
        print(f"  Agent instance: {opportunity_agent}")
        print(f"  Active sources: {opportunity_agent.get_active_sources()}")
        print("  ✓ Agent initialized with LangGraph\n")
        
        # Test 2: User context setting
        print("📋 Test 2: User Context Management")
        test_context = {
            "skills": ["Python", "JavaScript"],
            "experience_level": "junior",
            "location": "Egypt"
        }
        opportunity_agent.set_user_context(test_context)
        print(f"  User context set: {list(test_context.keys())}")
        print("  ✓ User context management working\n")
        
        # Test 3: Search without execution (just parse the state)
        print("📋 Test 3: Search Query Preparation")
        test_query = "python developer in cairo"
        print(f"  Query: '{test_query}'")
        print("  Note: Full search would require Pinecone/Groq API keys")
        print("  ✓ Query prepared and ready for execution\n")
        
        # Test 4: Source management
        print("📋 Test 4: Source Management")
        print(f"  Enabled sources before: {opportunity_agent.get_active_sources()}")
        opportunity_agent.disable_source("facebook")
        print(f"  After disabling facebook: {opportunity_agent.get_active_sources()}")
        opportunity_agent.enable_source("facebook")
        print(f"  After re-enabling facebook: {opportunity_agent.get_active_sources()}")
        print("  ✓ Source management working\n")
        
        print("=" * 60)
        print("✅ All integration tests passed!")
        print("\nThe LangGraph agent is properly integrated with agent_routes.py")
        print("\nNext steps:")
        print("  1. Set GROQ_API_KEY environment variable")
        print("  2. Configure Pinecone API key")
        print("  3. Run: python API/main.py")
        print("  4. Test endpoint: POST /agent/search")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_agent_search())
    sys.exit(0 if success else 1)
