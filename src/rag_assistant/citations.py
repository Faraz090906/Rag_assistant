import re


def cited_indices(answer):
    """Citation numbers like [2] that appear in the answer text."""
    return sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer or "")})


def split_citations(answer, hits):
    """Return (valid cited hits as (n, hit), invalid citation numbers)."""
    valid, invalid = [], []
    for n in cited_indices(answer):
        if 1 <= n <= len(hits):
            valid.append((n, hits[n - 1]))
        else:
            invalid.append(n)
    return valid, invalid
