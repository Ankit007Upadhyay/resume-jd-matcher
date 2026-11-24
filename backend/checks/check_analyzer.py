from app.services.analyzer import analyze, read_resume

JD = """We need an AI Engineer with Python and SQL skills.
Experience building RAG pipelines with vector databases such as FAISS is required.
Hands-on knowledge of Kubernetes and Docker is a must.
Bachelor's degree in Computer Science. Fine-tuning LLMs is a plus."""

# Test 1: galat file type
try:
    read_resume("resume.txt")
    raise AssertionError("txt reject hona chahiye tha")
except ValueError:
    print("txt sahi reject hua")

# Test 2: poora pipeline
report = analyze(r"..\sample.pdf", JD)

assert 0 <= report["final_score"] <= 100
assert report["verdict"] in ("Strong match", "Moderate match", "Weak match")
assert len(report["criteria"]) >= 3
assert "kubernetes" in report["skills"]["missing"]

print("Final:", report["final_score"], "|", report["verdict"])
print("Breakdown:", report["breakdown"]["components"])
print("Missing skills:", report["skills"]["missing"])

for c in report["criteria"]:
    print(f"\n{c['criterion']}")
    print(f"  llm={c['llm_score']} final_points={c['final_points']} found={c['found']} "
          f"grounded={c['grounded']} weak={c['weak_match']}")
    print(f"  evidence={c['evidence']!r}")

print("\nSab tests pass")