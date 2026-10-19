from . import config
from .ingest import load_pdfs
from .chunking import chunk_pages
from .vector_store import build_index, load_index
from .retriever import search
from .generator import generate
from .evidence import has_sufficient_evidence
from .citations import split_citations


def build(pdf_dir=config.PDF_DIR, index_dir=config.INDEX_DIR):
    pages = load_pdfs(pdf_dir)
    chunks = chunk_pages(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    if not chunks:
        raise RuntimeError(f"No text extracted from PDFs in {pdf_dir}")
    build_index(chunks, index_dir)
    return len(pages), len(chunks)


def answer(question, index, chunks, k=config.TOP_K, min_score=config.MIN_SCORE):
    """Retrieve, check evidence, generate. Returns a dict."""
    hits = search(question, index, chunks, k)
    if not has_sufficient_evidence(hits, min_score):
        return {"answer": config.NO_EVIDENCE_MSG, "hits": hits,
                "sufficient": False, "cited": [], "invalid_citations": []}
    text = generate(question, hits)  # None when no API key
    cited, invalid = split_citations(text, hits)
    return {"answer": text, "hits": hits, "sufficient": True,
            "cited": cited, "invalid_citations": invalid}


__all__ = ["build", "answer", "load_index"]
