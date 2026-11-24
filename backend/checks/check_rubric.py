from app.llm.schemas import CriterionResult
from app.scoring.rubric import is_grounded, rubric_score

resume = "Built an AI assistant combining RAG with a fine-tuned LLM to improve\ndomain-specific answer relevance."

# Test 1: grounded evidence (line break ke bawajood)
assert is_grounded("improve domain-specific answer relevance", resume) is True

# Test 2: bani hui quote
assert is_grounded("Deployed on Kubernetes at scale", resume) is False

# Test 3: khali evidence
assert is_grounded("", resume) is False

good = CriterionResult(criterion="RAG", score=8, evidence="combining RAG with a fine-tuned LLM", reasoning="x", found=True)
fake = CriterionResult(criterion="K8s", score=9, evidence="Deployed on Kubernetes", reasoning="x", found=True)
missing = CriterionResult(criterion="Docker", score=7, evidence="", reasoning="x", found=False)

# Test 4: grounded -> 80, bani quote -> cap 5 -> 50, found False -> 0
out = rubric_score([good, fake, missing], resume)
points = [d["final_points"] for d in out["details"]]
assert points == [80, 50, 0], points

# Test 5: average = (80 + 50 + 0) / 3
assert out["score"] == 43.3

# Test 6: khali list
assert rubric_score([], resume)["score"] == 0.0

print("Sab tests pass")