import os
from .config import LLM_MODEL


def build_prompt(question, hits):
    context = "\n\n".join(
        f"[{i}] ({h['source']}, p.{h['page']})\n{h['text']}"
        for i, h in enumerate(hits, 1))
    return ("Answer the question using ONLY the context below. Cite sources like [1]. "
            "If the context does not contain the answer, say you cannot find it.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}")


def generate(question, hits):
    """Call the LLM. Returns None if no API key is set."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        return None
    from anthropic import Anthropic
    r = Anthropic().messages.create(
        model=LLM_MODEL, max_tokens=500,
        messages=[{"role": "user", "content": build_prompt(question, hits)}])
    return r.content[0].text
