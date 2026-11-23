from pathlib import Path

from app.llm.chains import extract_criteria, score_criterion
from app.llm.schemas import CriterionResult
from app.parsing.cleaner import clean_text
from app.parsing.docx_parser import extract_text_from_docx
from app.parsing.pdf_parser import extract_text_from_pdf
from app.rag.retriever import retrieve_for_criteria
from app.rag.splitter import split_resume
from app.rag.vector_store import build_vector_store
from app.scoring.hybrid import hybrid_score
from app.scoring.rubric import rubric_score
from app.scoring.semantic import semantic_score
from app.scoring.skills import skill_overlap


def read_resume(file_path):
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif suffix == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Sirf .pdf ya .docx file allowed hai.")

    return clean_text(raw_text)


def safe_score(criterion, chunks):
    try:
        return score_criterion(criterion, chunks)
    except Exception as error:
        return CriterionResult(
            criterion=criterion,
            score=0,
            evidence="",
            reasoning=f"LLM call failed: {type(error).__name__}",
            found=False,
        )


def analyze_text(resume_text, jd_text):
    chunks = split_resume(resume_text)
    store = build_vector_store(chunks)

    criteria = extract_criteria(jd_text)
    retrievals = retrieve_for_criteria(store, criteria)
    results = [safe_score(r["criterion"], r["chunks"]) for r in retrievals]

    semantic = semantic_score(retrievals)
    skills = skill_overlap(jd_text, resume_text)
    rubric = rubric_score(results, resume_text)
    final = hybrid_score(semantic, skills["score"], rubric["score"])

    criteria_report = []
    for retrieval, detail in zip(retrievals, rubric["details"]):
        criteria_report.append(
            {
                **detail,
                "similarity": round(retrieval["top_score"], 3),
                "weak_match": retrieval["weak_match"],
            }
        )

    return {
        "final_score": final["final"],
        "verdict": final["verdict"],
        "breakdown": final,
        "criteria": criteria_report,
        "skills": skills,
        "num_chunks": len(chunks),
    }


def analyze(resume_path, jd_text):
    resume_text = read_resume(resume_path)
    return analyze_text(resume_text, jd_text)