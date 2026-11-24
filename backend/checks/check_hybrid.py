from app.scoring.hybrid import clamp_score, get_verdict, hybrid_score

# Test 1: wahi practice example (50, 90, 70)
r = hybrid_score(50, 90, 70)
assert r["final"] == 68.0, r["final"]

# Test 2: boundaries
assert hybrid_score(100, 100, 100)["final"] == 100.0
assert hybrid_score(0, 0, 0)["final"] == 0.0

# Test 3: clamp (range ke bahar)
assert clamp_score(150) == 100.0
assert clamp_score(-20) == 0.0
assert hybrid_score(150, 100, 100)["final"] == 100.0

# Test 4: contributions ka sum final ke aaspaas hona chahiye
c = r["contributions"]
assert abs(sum(c.values()) - r["final"]) < 0.2

# Test 5: verdict
assert get_verdict(80) == "Strong match"
assert get_verdict(60) == "Moderate match"
assert get_verdict(30) == "Weak match"

# Test 6: tumhare resume ke pichhle asli numbers
real = hybrid_score(49.5, 71.4, 43.3)
print(real)
assert real["final"] == 54.2, real["final"]

print("Sab tests pass")