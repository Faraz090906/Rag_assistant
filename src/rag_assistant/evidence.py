def has_sufficient_evidence(hits, min_score):
    """True if the best retrieved chunk is at least min_score (cosine)."""
    return bool(hits) and hits[0]["score"] >= min_score
