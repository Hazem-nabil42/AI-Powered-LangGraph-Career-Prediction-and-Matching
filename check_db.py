import os
import pickle
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "jobs-rag-egypt"

try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    print("Pinecone Stats:", stats)
except Exception as e:
    print("Error connecting to Pinecone:", e)

try:
    with open("database/bm25_index.pkl", "rb") as f:
        data = pickle.load(f)
        jobs = data.get("jobs", [])
        print("Local jobs count (BM25 pkl):", len(jobs))
        if jobs:
            print("Sample job keys:", list(jobs[0].keys()))
            print("Sample job date info:", jobs[0].get("time") or jobs[0].get("date") or "No explicit date field")
            # count how many have dates
            dates = [j.get("time") or j.get("date") for j in jobs if j.get("time") or j.get("date")]
            print(f"Jobs with date/time found: {len(dates)}")
except Exception as e:
    print("Error loading bm25 index:", e)
