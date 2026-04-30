import pickle

try:
    with open("database/bm25_index.pkl", "rb") as f:
        data = pickle.load(f)
        jobs = data.get("jobs", [])
        print("Sample 'posted' values:")
        sample_posted = [j.get("posted", "N/A") for j in jobs[:20]]
        for p in sample_posted:
            print("-", p)
except Exception as e:
    print("Error loading bm25 index:", e)
