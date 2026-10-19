import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from rag_assistant import config
from rag_assistant.pipeline import answer, load_index

index, chunks = load_index(config.INDEX_DIR)
while (q := input("\nQuestion (blank to quit): ").strip()):
    r = answer(q, index, chunks)
    print("\nANSWER:\n" + (r["answer"] or "(no API key set - retrieval only)"))
    if r["invalid_citations"]:
        print(f"WARNING: answer cites non-existent sources {r['invalid_citations']}")
    print("\nSOURCES CITED IN ANSWER:" if r["cited"] else "\nRETRIEVED SOURCES (none cited):")
    for n, h in (r["cited"] or list(enumerate(r["hits"], 1))):
        print(f"[{n}] {h['source']} p.{h['page']} (score {h['score']:.2f}): {h['text'][:120]!r}")
    if not r["sufficient"]:
        print("(top score below MIN_SCORE; LLM was not called)")
