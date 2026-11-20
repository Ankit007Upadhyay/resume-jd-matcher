from app.parsing.pdf_parser import extract_text_from_pdf
from app.parsing.cleaner import clean_text
from app.rag.splitter import split_resume
from app.rag.vector_store import build_vector_store
from app.rag.retriever import retrieve_for_criteria, format_context

text = clean_text(extract_text_from_pdf(r"..\sample.pdf"))
store = build_vector_store(split_resume(text))

criteria = [
    "Experience with RAG pipelines and vector databases",
    "Knowledge of Kubernetes and Docker",
    "Bachelor's degree in Computer Science",
]

for result in retrieve_for_criteria(store, criteria):
    print("\nCRITERION:", result["criterion"])
    print("top_score:", round(result["top_score"], 3), "| weak_match:", result["weak_match"])

print("\n===== LLM CONTEXT (criterion 1) =====")
first = retrieve_for_criteria(store, criteria[:1])[0]
print(format_context(first["chunks"]))