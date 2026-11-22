import os
from pathlib import Path

from dotenv import load_dotenv

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# ---------- LLM (Groq) ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-20b"
LLM_TEMPERATURE = 0

# ---------- Embeddings ----------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------- RAG settings ----------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3
WEAK_MATCH_SCORE = 0.25
# ---------- Hybrid score weights (total = 1.0) ----------
WEIGHT_SEMANTIC = 0.40
WEIGHT_SKILLS = 0.30
WEIGHT_RUBRIC = 0.30


SEMANTIC_LOW = 0.15
SEMANTIC_HIGH = 0.55



# ---------- Data files ----------
SKILLS_FILE = BASE_DIR / "backend" / "data" / "skills.txt"


def validate_config():
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY nahi mili. Root folder ki .env file check karo."
        )

    total = WEIGHT_SEMANTIC + WEIGHT_SKILLS + WEIGHT_RUBRIC
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Weights ka sum 1.0 hona chahiye, abhi {total} hai.")
    
    

