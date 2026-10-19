import pytest
from rag_assistant.chunking import chunk_pages
from rag_assistant.generator import build_prompt

PAGES = [{"source": "a.pdf", "page": 3, "text": "x" * 2000}]


def test_chunks_keep_metadata():
    for c in chunk_pages(PAGES, 800, 150):
        assert c["source"] == "a.pdf" and c["page"] == 3


def test_chunk_size_and_overlap():
    pages = [{"source": "a", "page": 1, "text": "".join(chr(97 + i % 26) for i in range(2000))}]
    cs = chunk_pages(pages, 800, 150)
    assert all(len(c["text"]) <= 800 for c in cs)
    assert cs[0]["text"][-150:] == cs[1]["text"][:150]


def test_no_trailing_duplicate_chunk():
    cs = chunk_pages([{"source": "a", "page": 1, "text": "y" * 500}], 800, 150)
    assert len(cs) == 1


def test_bad_overlap():
    with pytest.raises(ValueError):
        chunk_pages(PAGES, 100, 100)


def test_prompt_contains_citation_and_question():
    p = build_prompt("What?", [{"source": "a.pdf", "page": 2, "text": "hello"}])
    assert "[1] (a.pdf, p.2)" in p and "What?" in p
