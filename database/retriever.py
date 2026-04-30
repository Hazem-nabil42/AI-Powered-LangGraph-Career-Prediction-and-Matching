# database/retriever.py
"""
Unified Retriever Interface
Automatically switches between Chroma and Pinecone based on VECTOR_DB_TYPE
Supports hybrid search with BM25 fallback
"""

import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

# Configuration
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "pinecone").lower()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "jobs-rag-egypt")

print(f"🔌 Using Vector DB: {VECTOR_DB_TYPE.upper()}")

# Import appropriate retriever
if VECTOR_DB_TYPE == "pinecone" and PINECONE_API_KEY:
    try:
        from database.pinecone_retriever import hybrid_search, simple_vector_search
        print("✅ Pinecone retriever loaded")
        ACTIVE_RETRIEVER = "pinecone"
    except Exception as e:
        print(f"⚠️  Pinecone failed: {e}, falling back to Chroma")
        from database.hybrid_retriever import hybrid_search
        ACTIVE_RETRIEVER = "chroma"
else:
    from database.hybrid_retriever import hybrid_search
    print("✅ Chroma retriever loaded")
    ACTIVE_RETRIEVER = "chroma"


def search(query: str, n_results: int = 15) -> List[Dict[str, Any]]:
    """
    Unified search interface
    
    Args:
        query: Search query string
        n_results: Number of results to return
    
    Returns:
        List of job results with scores
    """
    return hybrid_search(query, n_results=n_results)


def get_active_db() -> str:
    """Returns the currently active database type"""
    return ACTIVE_RETRIEVER


if __name__ == "__main__":
    # Test search
    results = search("python developer", n_results=5)
    print(f"\n✅ Search successful! Found {len(results)} results")
