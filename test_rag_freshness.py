#!/usr/bin/env python3
"""
Test suite for RAG pipeline with freshness filtering
Tests data freshness and multi-source routing
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.langgraph_agents.opportunity_agent import OpportunityAgent
from database.pinecone_retriever import is_job_fresh


def test_freshness_filter():
    """Test the freshness filter function."""
    print("\n" + "="*70)
    print("🧪 TEST 1: Job Freshness Filter")
    print("="*70)
    
    test_cases = [
        {
            "job": {"title": "Python Dev", "posted": "2 days ago"},
            "expected": True,
            "description": "Recent job (2 days)"
        },
        {
            "job": {"title": "JS Dev", "posted": "1 week ago"},
            "expected": True,
            "description": "Recent job (1 week)"
        },
        {
            "job": {"title": "Data Scientist", "posted": "2 months ago"},
            "expected": False,
            "description": "Old job (2 months)"
        },
        {
            "job": {"title": "ML Engineer", "posted": "1 year ago"},
            "expected": False,
            "description": "Very old job (1 year)"
        },
        {
            "job": {"title": "DevOps", "posted": "3 hours ago"},
            "expected": True,
            "description": "Very recent job (3 hours)"
        },
        {
            "job": {"title": "QA Engineer", "posted": "1 month ago"},
            "expected": False,
            "description": "Exactly 1 month old"
        },
        {
            "job": {"title": "Product Manager", "posted": "Recently"},
            "expected": True,
            "description": "Recently posted"
        },
        {
            "job": {"title": "Sales", "posted": "Now"},
            "expected": True,
            "description": "Just posted"
        },
        {
            "job": {"title": "Backend Dev", "time": "5 days ago"},
            "expected": True,
            "description": "Using 'time' field instead of 'posted'"
        },
        {
            "job": {"title": "Frontend Dev", "date": "3 weeks ago"},
            "expected": True,
            "description": "Using 'date' field instead of 'posted'"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        job = test_case["job"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        result = is_job_fresh(job)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        print(f"\n{i}. {description}")
        print(f"   Job: {job.get('title', 'N/A')}")
        print(f"   Posted: {job.get('posted') or job.get('time') or job.get('date', 'N/A')}")
        print(f"   Expected: {expected}, Got: {result} {status}")
        
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'─'*70}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    return failed == 0


async def test_multi_source_routing():
    """Test multi-source routing via LangGraph."""
    print("\n" + "="*70)
    print("🧪 TEST 2: Multi-Source LangGraph Routing")
    print("="*70)
    
    agent = OpportunityAgent()
    
    test_queries = [
        {
            "query": "python developer",
            "expected_sources": ["linkedin"],
            "description": "General tech job"
        },
        {
            "query": "ITI course for python",
            "expected_sources": ["iti_nti"],
            "description": "ITI/NTI course request"
        },
        {
            "query": "facebook group for job postings",
            "expected_sources": ["facebook"],
            "description": "Facebook groups"
        },
        {
            "query": "internship at google careers page",
            "expected_sources": ["companies", "linkedin"],
            "description": "Company careers page"
        },
        {
            "query": "volunteering opportunities",
            "expected_sources": ["volunteering"],
            "description": "Volunteering search"
        },
    ]
    
    print("\nTesting query routing (this may take a moment)...\n")
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        expected = test_case["expected_sources"]
        description = test_case["description"]
        
        print(f"{i}. {description}")
        print(f"   Query: '{query}'")
        print(f"   Expected sources: {expected}")
        
        try:
            result = await agent.search_opportunities(query)
            
            sources_used = result.get("sources_used", [])
            total_results = result.get("total_results", 0)
            
            print(f"   Sources used: {sources_used}")
            print(f"   Results found: {total_results}")
            
            if sources_used:
                print(f"   ✅ Routing worked!")
            else:
                print(f"   ⚠️  No sources were used")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    return True


async def test_integration():
    """Run a full integration test."""
    print("\n" + "="*70)
    print("🧪 TEST 3: Full Integration Test")
    print("="*70)
    
    agent = OpportunityAgent()
    
    # Set user context
    user_context = {
        "skills": ["Python", "JavaScript", "React"],
        "experience_level": "junior",
        "location": "Cairo",
        "preferred_roles": ["Frontend Developer", "Full Stack Developer"]
    }
    
    agent.set_user_context(user_context)
    
    print(f"\n📋 User Context Set:")
    print(f"   Skills: {user_context['skills']}")
    print(f"   Experience: {user_context['experience_level']}")
    print(f"   Location: {user_context['location']}")
    
    print(f"\n🔍 Running search: 'Frontend developer jobs Cairo'")
    
    try:
        result = await agent.search_opportunities(
            query="Frontend developer jobs Cairo",
            opportunity_type="jobs",
            filters={"location": "Cairo"}
        )
        
        print(f"\n✅ Search completed successfully!")
        print(f"   Total results: {result['total_results']}")
        print(f"   Sources used: {result['sources_used']}")
        print(f"   Reasoning (first 200 chars): {result['reasoning'][:200]}...")
        
        if result['total_results'] > 0:
            first_opp = result['opportunities'][0]
            print(f"\n   First result:")
            print(f"   - Title: {first_opp['title']}")
            print(f"   - Company: {first_opp['company']}")
            print(f"   - Source: {first_opp['source']}")
            print(f"   - Score: {first_opp['score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  RAG PIPELINE FRESHNESS & LANGGRAPH ROUTING TESTS  ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    results = {
        "freshness": test_freshness_filter(),
        "routing": asyncio.run(test_multi_source_routing()),
        "integration": asyncio.run(test_integration()),
    }
    
    print("\n" + "="*70)
    print("📊 FINAL RESULTS")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ All tests passed! RAG pipeline is ready to use.")
    else:
        print("❌ Some tests failed. Check the output above.")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
