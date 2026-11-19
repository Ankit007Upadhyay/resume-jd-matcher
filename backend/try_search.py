from app.parsing.pdf_parser import extract_text_from_pdf
from app.parsing.cleaner import clean_text
from app.rag.splitter import split_resume
from app.rag.vector_store import build_vector_store, search_store

text = clean_text(extract_text_from_pdf(r"..\sample.pdf"))
chunks = split_resume(text)
store = build_vector_store(chunks)

queries = [
    "Which vector databases does the candidate know?",
    "Where did the candidate work as an intern?",
    "Does the candidate know Kubernetes?",
]

for query in queries:
    print("\nQUERY:", query)
    for r in search_store(store, query):
        print(f"  chunk {r['chunk_id']} | score {r['score']:.3f} | {r['text'][:70]!r}")