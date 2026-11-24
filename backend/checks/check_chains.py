from app.llm.chains import extract_criteria, score_criterion
from app.parsing.pdf_parser import extract_text_from_pdf
from app.parsing.cleaner import clean_text
from app.rag.splitter import split_resume
from app.rag.vector_store import build_vector_store
from app.rag.retriever import retrieve_for_criterion

jd = """We need an AI Engineer with Python and SQL skills.
Experience building RAG pipelines with vector databases such as FAISS is required.
Hands-on knowledge of Kubernetes and Docker is a must.
Bachelor's degree in Computer Science. Fine-tuning LLMs is a plus."""

print("JD length:", len(jd))
print(repr(jd[:80]))
criteria = extract_criteria(jd)
print("Criteria:", criteria)
assert 3 <= len(criteria) <= 8

store = build_vector_store(split_resume(clean_text(extract_text_from_pdf(r"..\sample.pdf"))))

resume_text = clean_text(extract_text_from_pdf(r"..\sample.pdf"))

for c in criteria:
    r = retrieve_for_criterion(store, c)
    res = score_criterion(c, r["chunks"])
    print(f"\n{c}\n  score={res.score} found={res.found}\n  evidence={res.evidence!r}")
    if res.evidence:
        print("  grounded:", res.evidence.lower() in resume_text.lower())