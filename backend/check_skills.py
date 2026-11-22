from app.scoring.skills import find_skills, skill_overlap
from app.parsing.pdf_parser import extract_text_from_pdf
from app.parsing.cleaner import clean_text


print(repr(find_skills("I use docker daily")))
# Test 1: substring bug nahi hona chahiye
assert find_skills("I use docker daily") == {"docker"}
assert "java" not in find_skills("I know javascript")
assert "javascript" in find_skills("I know javascript")

# Test 2: special characters
assert "c++" in find_skills("Experienced in C++, Python.")
assert "node.js" in find_skills("Built APIs with Node.js")

# Test 3: score math
r = skill_overlap("python sql docker kubernetes", "I know python and sql")
assert r["score"] == 50.0
assert r["missing"] == ["docker", "kubernetes"]

# Test 4: JD mein koi skill nahi
assert skill_overlap("be a nice person", "python")["score"] == 0.0

# Test 5: asli resume
jd = """We need an AI Engineer with Python and SQL skills.
Experience building RAG pipelines with vector databases such as FAISS is required.
Hands-on knowledge of Kubernetes and Docker is a must.
Bachelor's degree in Computer Science. Fine-tuning LLMs is a plus."""
resume = clean_text(extract_text_from_pdf(r"..\sample.pdf"))
print(skill_overlap(jd, resume))

print("Sab tests pass")