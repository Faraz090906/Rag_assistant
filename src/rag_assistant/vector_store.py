import json
from pathlib import Path
import faiss
from .embeddings import embed


def make_index(chunks):
    """Embed chunks and return an in-memory FAISS index."""
    vecs = embed([c["text"] for c in chunks])
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    return index


def build_index(chunks, index_dir):
    index_dir = Path(index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    index = make_index(chunks)
    faiss.write_index(index, str(index_dir / "index.faiss"))
    (index_dir / "chunks.json").write_text(json.dumps(chunks))


def load_index(index_dir):
    index_dir = Path(index_dir)
    index = faiss.read_index(str(index_dir / "index.faiss"))
    chunks = json.loads((index_dir / "chunks.json").read_text())
    return index, chunks
