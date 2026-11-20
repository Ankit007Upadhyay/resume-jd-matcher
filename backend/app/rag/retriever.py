from app.config import WEAK_MATCH_SCORE, TOP_K
from app.rag.vector_store import search_store

def retrieve_for_criterion(store, criterion,k=TOP_K):
    chunks = search_store(store, criterion, k=k)
    top_score = chunks[0]["score"] if chunks else 0.0
    
    return {
        "chunks": chunks,
        "top_score": top_score,
        "criterion": criterion,
        "weak_match": top_score < WEAK_MATCH_SCORE,
    }
    
    
def retrieve_for_criteria(store, criteria, k=TOP_K):
    return [retrieve_for_criterion(store, c, k=k) for c in criteria]


def format_context(chunks):
    if not chunks:
        return "no relevant resume text found"
    
    parts = [f"[Chunk {c['chunk_id']}]\n{c['text']}" for c in chunks]
    return "\n\n".join(parts)