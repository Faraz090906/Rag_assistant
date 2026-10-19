from rag_assistant.evidence import has_sufficient_evidence
from rag_assistant.citations import cited_indices, split_citations
from rag_assistant.metrics import recall_at_k, mrr

H = [{"source": "a.pdf", "page": 1, "score": 0.8}, {"source": "a.pdf", "page": 5, "score": 0.4}]
Q = {"expected_source": "a.pdf", "expected_pages": [5]}


def test_evidence_threshold():
    assert has_sufficient_evidence(H, 0.5)
    assert not has_sufficient_evidence(H, 0.9)
    assert not has_sufficient_evidence([], 0.1)


def test_cited_indices_and_invalid():
    assert cited_indices("See [2] and [1], also [2].") == [1, 2]
    valid, invalid = split_citations("x [1] y [7]", H)
    assert [n for n, _ in valid] == [1] and invalid == [7]


def test_recall_and_mrr():
    res = [(Q, H)]
    assert recall_at_k(res, 1) == 0.0
    assert recall_at_k(res, 2) == 1.0
    assert mrr(res) == 0.5
    assert recall_at_k([], 3) == 0.0
