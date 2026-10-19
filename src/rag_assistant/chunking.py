def chunk_pages(pages, size=800, overlap=150):
    """Split each page into overlapping character windows; keep source/page."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    step = size - overlap
    chunks = []
    for pg in pages:
        text = pg["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + size].strip()
            if piece:
                chunks.append({"source": pg["source"], "page": pg["page"], "text": piece})
            if start + size >= len(text):
                break
    return chunks
