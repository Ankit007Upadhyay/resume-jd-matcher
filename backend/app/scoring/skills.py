import re
from app.config import SKILLS_FILE
from functools import lru_cache


@lru_cache(maxsize=1)
def load_skills():
    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip().lower() for line in f ]
    return [line for line in lines if line]



def find_skills(text):
    text = text.lower()
    found = set()
    for skill in load_skills():
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.add(skill)
    return found
    
    
def skill_overlap(jd_text, resume_text):
    required = find_skills(jd_text)
    if not required:
         return {"score": 0.0, "required": [], "matched": [], "missing": []}

    resume_skills = find_skills(resume_text)
    matched = required & resume_skills
    missing = required - resume_skills
    
    return {
        "score": round(len(matched) / len(required) * 100, 1),
        "required": sorted(required),
        "matched": sorted(matched),
        "missing": sorted(missing),
    }