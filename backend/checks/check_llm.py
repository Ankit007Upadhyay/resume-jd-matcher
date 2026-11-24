from app.llm.client import get_llm

llm = get_llm()

# Test 1: kya object cache hota hai?
assert get_llm() is llm, "Dono calls par same object aana chahiye"

# Test 2: asli call
response = llm.invoke("Reply with exactly one word: hello")
print("Reply:", response.content)

# Test 3: reply khali nahi hona chahiye
assert response.content.strip(), "LLM ne khali reply diya"

print("Sab tests pass")