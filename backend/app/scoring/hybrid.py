from app.config import WEIGHT_RUBRIC, WEIGHT_SEMANTIC, WEIGHT_SKILLS


def clamp_score(value):
    return max(0.0, min(100.0, float(value)))


def get_verdict(final):
    if final >= 75:
        return "Strong match"
    if final >= 50:
        return "Moderate match"
    return "Weak match"


def hybrid_score(semantic, skills, rubric):
    semantic = clamp_score(semantic)
    skills = clamp_score(skills)
    rubric = clamp_score(rubric)

    semantic_part = semantic * WEIGHT_SEMANTIC
    skills_part = skills * WEIGHT_SKILLS
    rubric_part = rubric * WEIGHT_RUBRIC

    final = round(semantic_part + skills_part + rubric_part, 1)

    return {
        "final": final,
        "verdict": get_verdict(final),
        "components": {
            "semantic": semantic,
            "skills": skills,
            "rubric": rubric,
        },
        "contributions": {
            "semantic": round(semantic_part, 1),
            "skills": round(skills_part, 1),
            "rubric": round(rubric_part, 1),
        },
        "weights": {
            "semantic": WEIGHT_SEMANTIC,
            "skills": WEIGHT_SKILLS,
            "rubric": WEIGHT_RUBRIC,
        },
    }