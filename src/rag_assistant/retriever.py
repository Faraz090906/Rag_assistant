from .embeddings import embed


def search(question, index, chunks, k=4):
    """Top-k chunks by cosine similarity, with scores."""
    scores, ids = index.search(embed([question]), k)
    return [{**chunks[i], "score": float(s)}
            for s, i in zip(scores[0], ids[0]) if i != -1]
