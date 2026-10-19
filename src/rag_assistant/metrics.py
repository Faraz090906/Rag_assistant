def is_hit(hit, q):
    """Page-level match, so results are comparable across chunk sizes."""
    return hit["source"] == q["expected_source"] and hit["page"] in q["expected_pages"]


def recall_at_k(results, k):
    """results: list of (question, hits). Fraction with a correct hit in top k."""
    if not results:
        return 0.0
    return sum(any(is_hit(h, q) for h in hits[:k]) for q, hits in results) / len(results)


def mrr(results):
    """Mean reciprocal rank of the first correct hit (0 if none retrieved)."""
    if not results:
        return 0.0
    total = 0.0
    for q, hits in results:
        for rank, h in enumerate(hits, 1):
            if is_hit(h, q):
                total += 1 / rank
                break
    return total / len(results)
