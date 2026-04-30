import fitz 
import math 
from sentence_transformers import SentenceTransformer 
from groq import Groq 
import sys, os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from dotenv import load_dotenv 
# fresh jobs date filter
from datetime import datetime, timedelta

load_dotenv() 

# Initialize Groq client with API key
client = Groq(api_key=os.getenv("GROQ_API_KEY")) 
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') 

# Initialize Pinecone (with fallback to Chroma)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "pinecone").lower()

if VECTOR_DB_TYPE == "pinecone" and PINECONE_API_KEY:
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        pinecone_index = pc.Index(os.getenv("PINECONE_INDEX_NAME", "jobs-rag-egypt"))
        use_pinecone = True
        print("✅ Using Pinecone vector database")
    except Exception as e:
        print(f"⚠️  Pinecone failed: {e}, falling back to Chroma")
        import chromadb
        db_client = chromadb.PersistentClient(path="database/chroma_db") 
        collection = db_client.get_collection("jobs")
        use_pinecone = False
else:
    import chromadb
    db_client = chromadb.PersistentClient(path="database/chroma_db") 
    collection = db_client.get_collection("jobs")
    use_pinecone = False 

# Fresh and open jobs filter
def is_recent_and_open(job):
    status = job.get('status', '').lower()
    posted_date_str = job.get('posted_date', '')
    
    if status != 'open':
        return False
    
    if posted_date_str:
        posted_date = datetime.strptime(posted_date_str, "%Y-%m-%d")
        today = datetime.now()
        if (today - posted_date) <= timedelta(days=14):  # فقط من آخر أسبوعين
            return True
    return False

def extract_text_from_pdf(pdf_bytes): 
    """Extracts text from uploaded PDF bytes."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf") 
    text = "" 
    for page in doc: 
        text += page.get_text() 
    return text.strip() 

def extract_skills_from_cv(cv_text): 
    """
    Uses Groq LLM to extract key skills, technologies, and experience 
    from the full CV text to optimize vector embeddings.
    """
    prompt = f"""
    Analyze the following resume text and extract the key technical skills, 
    job titles, and years of experience. Provide a concise summary 
    suitable for job matching.
    
    Resume Text:
    {cv_text}
    """
    
    response = client.chat.completions.create( 
        model="llama-3.1-8b-instant", 
        messages=[{
            "role": "user",
            "content": f"""من الـ CV ده، استخرج:
1. المسمى الوظيفي المناسب
2. المهارات التقنية
3. سنوات الخبرة
4. المجال

رد بالإنجليزي فقط في صيغة:
Job Title: ...
Skills: skill1, skill2, skill3, ...
Experience: X years
Field: ...

CV:
{cv_text[:3000]}"""
        }],
        max_tokens=200
    )

    extracted = response.choices[0].message.content
    print(f"📋 Extracted profile:\n{extracted}\n")
    return extracted


def distance_to_score(distance):
    return round(math.exp(-distance / 10) * 100, 1)


def match_cv_to_jobs(pdf_bytes, n_results=5):
    # ── 1. استخرج النص ──
    cv_text = extract_text_from_pdf(pdf_bytes)
    if not cv_text:
        return [], "مش قادر أقرأ الـ CV"

    print(f"📄 CV text: {len(cv_text)} chars")

    # ── 2. استخرج الـ skills بالـ LLM ──
    skills_profile = extract_skills_from_cv(cv_text)

    # ── 3. حول الـ profile للـ vector (مش الـ CV كامل) ──
    cv_vector = model.encode(skills_profile).tolist()

    # ── 4. دور في الـ DB (Pinecone or Chroma) ──
    if use_pinecone:
        # Query Pinecone
        results = pinecone_index.query(
            vector=cv_vector,
            top_k=n_results,
            include_metadata=True
        )
        
        distances = []
        metadatas = []
        for match in results.matches:
            # Pinecone returns similarity scores (0-1), convert to distance
            distance = 1 - match.score
            distances.append(distance)
            metadatas.append(match.metadata)
    else:
        # Query Chroma
        results = collection.query(
            query_embeddings=[cv_vector],
            n_results=n_results
        )
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]

    print(f"Raw distances: {[round(d,2) for d in distances]}")

    # ── 5. احسب الـ scores ──
    matches = [m for m in matches if is_recent_and_open(m)]
    for i, metadata in enumerate(metadatas):
        matches.append({
            "title":      metadata.get("title", "N/A"),
            "company":    metadata.get("company", "N/A"),
            "location":   metadata.get("location", "N/A"),
            "experience": metadata.get("experience", "N/A"),
            "level":      metadata.get("level", "N/A"),
            "job_type":   metadata.get("job_type", "N/A"),
            "url":        metadata.get("url", "#"),
            "source":     metadata.get("source", "wuzzuf"),
            "match":      distance_to_score(distances[i])
        })

    # ── 6. normalize الـ scores بين 60% و 99% ──
    # عشان الـ scores تبان منطقية للمستخدم
    if matches:
        max_score = max(m['match'] for m in matches)
        min_score = min(m['match'] for m in matches)

        for m in matches:
            if max_score != min_score:
                normalized = 60 + ((m['match'] - min_score) / (max_score - min_score)) * 39
                m['match'] = round(normalized, 1)
            else:
                m['match'] = 75.0

    matches.sort(key=lambda x: x['match'], reverse=True)
    return matches, skills_profile


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "rb") as f:
            pdf_bytes = f.read()

        matches, profile = match_cv_to_jobs(pdf_bytes)
        print(f"\n🎯 Top matches:")
        for m in matches:
            print(f"  {m['match']}% | {m['title']} @ {m['company']}")