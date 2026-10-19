"""Compare chunk size / overlap / top-k. Needs data/eval/questions.json (you write it)."""
import sys, json, csv, itertools, statistics, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from rag_assistant import config
from rag_assistant.ingest import load_pdfs
from rag_assistant.chunking import chunk_pages
from rag_assistant.vector_store import make_index
from rag_assistant.retriever import search
from rag_assistant.metrics import recall_at_k, mrr

SIZES, OVERLAPS, KS = [400, 800, 1200], [0, 100, 200], [1, 2, 4, 6]

if not config.EVAL_FILE.exists():
    sys.exit(f"Missing {config.EVAL_FILE}. Copy questions.example.json and write real, verified questions.")
questions = json.loads(config.EVAL_FILE.read_text())
ans_q = [q for q in questions if q["answerable"]]
unans_q = [q for q in questions if not q["answerable"]]
if not ans_q:
    sys.exit("Need at least one answerable question.")
pages = load_pdfs(config.PDF_DIR)

rows = []
for size, ov in itertools.product(SIZES, OVERLAPS):
    if ov >= size:
        continue
    chunks = chunk_pages(pages, size, ov)
    index = make_index(chunks)
    kmax = max(KS)
    res = [(q, search(q["question"], index, chunks, kmax)) for q in ans_q]
    un_top = [search(q["question"], index, chunks, 1)[0]["score"] for q in unans_q]
    top_ans = [h[0]["score"] for _, h in res if h]
    for k in KS:
        rows.append({"chunk_size": size, "overlap": ov, "k": k, "n_chunks": len(chunks),
                     "recall_at_k": round(recall_at_k(res, k), 3), "mrr": round(mrr(res), 3),
                     "mean_top1_score_answerable": round(statistics.mean(top_ans), 3),
                     "mean_top1_score_unanswerable": round(statistics.mean(un_top), 3) if un_top else ""})
    print(f"done size={size} overlap={ov}")

config.RESULTS_DIR.mkdir(exist_ok=True)
out = config.RESULTS_DIR / "retrieval_experiments.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"\n{len(ans_q)} answerable, {len(unans_q)} unanswerable questions -> {out}")
for r in sorted(rows, key=lambda r: (-r["recall_at_k"], r["k"]))[:5]:
    print(r)
