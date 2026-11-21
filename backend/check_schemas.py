from pydantic import ValidationError
from app.llm.schemas import CriterionResult, JDCriteria

# Test 1: sahi data
ok = CriterionResult(criterion="RAG", score=8, evidence="Built RAG assistant", reasoning="clear", found=True)
assert ok.score == 8

# Test 2: score 15 reject hona chahiye
try:
    CriterionResult(criterion="RAG", score=15, reasoning="x", found=True)
    raise AssertionError("score=15 reject hona chahiye tha")
except ValidationError:
    print("score=15 sahi reject hua")

# Test 3: evidence na do to default chalna chahiye
no_ev = CriterionResult(criterion="K8s", score=0, reasoning="not in resume", found=False)
assert no_ev.evidence == ""

# Test 4: JSON se object banana (LLM yahi dega)
parsed = CriterionResult.model_validate_json(
    '{"criterion":"SQL","score":7,"evidence":"Text-to-SQL","reasoning":"ok","found":true}'
)
assert parsed.found is True

# Test 5: list wala model
assert len(JDCriteria(criteria=["a", "b"]).criteria) == 2

print("Sab tests pass")