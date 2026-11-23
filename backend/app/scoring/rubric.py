import re

from app.config import UNGROUNDED_SCORE_CAP


def normalize_for_match(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def is_grounded(evidence, resume_text):
    if not evidence or not evidence.strip():
        return False
    return normalize_for_match(evidence) in normalize_for_match(resume_text)


def rubric_score(results, resume_text):
    if not results:
        return {"score": 0.0, "details": []}

    details = []
    for r in results:
        if not r.found:
            grounded = False
            raw = 0
        else:
            grounded = is_grounded(r.evidence, resume_text)
            raw = r.score if grounded else min(r.score, UNGROUNDED_SCORE_CAP)

        details.append(
            {
                "criterion": r.criterion,
                "llm_score": r.score,
                "final_points": raw * 10,
                "found": r.found,
                "grounded": grounded,
                "evidence": r.evidence,
            }
        )

    average = sum(d["final_points"] for d in details) / len(details)
    return {"score": round(average, 1), "details": details}