from app.config import SEMANTIC_HIGH, SEMANTIC_LOW


def normalize_similarity(similarity):
    span = SEMANTIC_HIGH - SEMANTIC_LOW
    scaled = (similarity - SEMANTIC_LOW) / span
    clamped = max(0.0, min(1.0, scaled))
    return round(clamped * 100, 1)


def semantic_score(retrievals):
    if not retrievals:
        return 0.0

    scores = [normalize_similarity(r["top_score"]) for r in retrievals]
    return round(sum(scores) / len(scores), 1)