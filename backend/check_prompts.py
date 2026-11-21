from app.llm.prompts import criteria_prompt, rubric_prompt

# Test 1: variables sahi hain?
assert set(criteria_prompt.input_variables) == {"jd_text"}
assert set(rubric_prompt.input_variables) == {"criterion", "context"}

# Test 2: variables bharne par messages bante hain?
messages = rubric_prompt.format_messages(
    criterion="Experience with RAG pipelines",
    context="[Chunk 1]\nBuilt a RAG assistant",
)
assert len(messages) == 2

# Test 3: asli values prompt mein aayi?
assert "Experience with RAG pipelines" in messages[1].content
assert "Built a RAG assistant" in messages[1].content

print(messages[0].content[:200])
print("Sab tests pass")