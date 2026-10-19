import numpy as np
from .config import EMBED_MODEL

_model = None


def embed(texts):
    """Return normalized float32 embeddings (cosine == inner product)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL)
    vecs = _model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(vecs, dtype="float32")
