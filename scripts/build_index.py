import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from rag_assistant.pipeline import build

pages, chunks = build()
print(f"Indexed {chunks} chunks from {pages} pages")
