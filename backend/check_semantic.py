from app.scoring.semantic import normalize_similarity, semantic_score
from app.parsing.pdf_parser import extract_text_from_pdf
from app.parsing.cleaner import clean_text
from app.rag.splitter import split_resume
from app.rag.vector_store import build_vector_store
from app.rag.retriever import retrieve_for_criteria

# Test 1: boundaries
assert normalize_similarity(0.15) == 0.0
assert normalize_similarity(0.55) == 100.0
assert normalize_similarity(0.35) == 50.0

# Test 2: clamp (range ke bahar)
assert normalize_similarity(0.9) == 100.0
assert normalize_similarity(-0.2) == 0.0

# Test 3: khali list
assert semantic_score([]) == 0.0

# Test 4: average
fake = [{"top_score": 0.15}, {"top_score": 0.55}]
assert semantic_score(fake) == 50.0

# Test 5: asli resume
store = build_vector_store(split_resume(clean_text(extract_text_from_pdf(r"..\sample.pdf"))))
criteria = [
    "Experience with RAG pipelines and vector databases",
    "Bachelor's degree in Computer Science",
    "Knowledge of Kubernetes and Docker",
]
retrievals = retrieve_for_criteria(store, criteria)
for r in retrievals:
    print(round(r["top_score"], 3), "->", normalize_similarity(r["top_score"]), "|", r["criterion"])
print("Semantic score:", semantic_score(retrievals))

print("Sab tests pass")