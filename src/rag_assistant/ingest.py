from pathlib import Path
from pypdf import PdfReader


def load_pdfs(folder):
    """Return a list of {source, page, text} dicts, one per non-empty page."""
    pages = []
    for p in sorted(Path(folder).glob("*.pdf")):
        for i, page in enumerate(PdfReader(p).pages, 1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append({"source": p.name, "page": i, "text": text})
    return pages
