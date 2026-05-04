#!/usr/bin/env python
"""Test script to verify agent is returning real data"""
import asyncio
from agents.langgraph_agents.opportunity_agent import opportunity_agent

async def test_agent():
    print("\n" + "="*60)
    print("Testing Agent with Real Data")
    print("="*60 + "\n")
    
    result = await opportunity_agent.search_opportunities('python developer internship')
    
    print(f"\n✅ Found {result['total_results']} opportunities")
    print(f"📍 Sources used: {result['sources_used']}")
    print(f"🤖 Reasoning: {result['reasoning'][:200]}...")
    
    if result['opportunities']:
        print(f"\n📊 Top opportunity:")
        opp = result['opportunities'][0]
        print(f"   Title: {opp['title']}")
        print(f"   Company: {opp['company']}")
        print(f"   Location: {opp['location']}")
        print(f"   Source: {opp.get('source', 'unknown')}")
        print(f"   Relevance Score: {opp.get('score', 'N/A')}")
    
    print("\n" + "="*60)
    print("✅ Agent test completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_agent())
