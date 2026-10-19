# Modular RAG Assistant for Technical PDFs

A student project: a command-line assistant that answers questions from technical PDF documents using Retrieval-Augmented Generation (RAG), with source citations and a "not enough evidence" guard.

> **Project status (read this first):** Months 1 and 2 are *implemented in code*. Unit tests for the pure-logic parts pass. The full pipeline (embeddings, FAISS, LLM) and the retrieval experiments have **not yet been run on real PDFs**, so this repository contains **no experimental results yet**. Results will be added to `results/` and this README only after they are actually produced. See [PROGRESS.md](PROGRESS.md).

## What it does
1. Loads technical PDFs and extracts text per page.
2. Splits pages into overlapping character chunks, keeping source file and page number.
3. Embeds chunks with `sentence-transformers/all-MiniLM-L6-v2` and stores them in a FAISS index.
4. Retrieves the top-k chunks for a question.
5. If the best chunk's similarity is below a threshold, it declines to answer instead of calling the LLM.
6. Otherwise it asks an LLM (Anthropic API) to answer using only the retrieved context, citing sources like `[1]`.
7. Shows which sources the answer actually cited and warns about citations that do not exist.

## Repository structure
```
rag-assistant/
├── README.md
├── PROGRESS.md                  honest progress log
├── requirements.txt
├── .env.example                 copy to .env; never commit real keys
├── .gitignore
├── data/
│   ├── pdfs/                    put your PDFs here (git-ignored)
│   └── eval/
│       ├── questions.example.json   template for the evaluation set
│       └── questions.json           YOU create this (verified questions)
├── src/rag_assistant/
│   ├── config.py                chunk size, top-k, models, MIN_SCORE
│   ├── ingest.py                PDF -> page text
│   ├── chunking.py              overlapping chunks with metadata
│   ├── embeddings.py            normalized sentence embeddings
│   ├── vector_store.py          FAISS build / save / load
│   ├── retriever.py             top-k search
│   ├── evidence.py              sufficient-evidence check
│   ├── generator.py             prompt + LLM call
│   ├── citations.py             parse [n] citations, flag invalid ones
│   ├── metrics.py               Recall@k and MRR
│   └── pipeline.py              build + answer orchestration
├── scripts/
│   ├── build_index.py           index the PDFs
│   ├── ask.py                   interactive Q&A
│   └── run_experiments.py       compare chunk size / overlap / k
├── tests/                       unit tests (pytest)
└── results/                     experiment outputs (CSV) after you run them
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key  # optional: without it you get retrieval only
```
The first run downloads the embedding model (~90 MB).

## Usage
```bash
python scripts/build_index.py      # index data/pdfs
python scripts/ask.py              # ask questions
pytest                             # run tests
```

### Running the retrieval experiments (Month 2)
1. Copy `data/eval/questions.example.json` to `data/eval/questions.json`.
2. Write 15-25 questions. For each answerable one, open the PDF yourself and record the file and page(s) that contain the answer. Add 3-5 unanswerable questions (`"answerable": false`).
3. Run:
```bash
python scripts/run_experiments.py
```
This tests chunk sizes 400/800/1200, overlaps 0/100/200 and k = 1/2/4/6, and writes `results/retrieval_experiments.csv` with Recall@k, MRR and mean top-1 scores for answerable vs unanswerable questions.
4. Use the score gap between answerable and unanswerable questions to choose `MIN_SCORE` in `config.py`. The default 0.30 is only a starting guess.

## Design choices
| Choice | Reason | Trade-off |
|---|---|---|
| Fixed-size character chunks with overlap | Simple, predictable, easy to explain | May cut mid-sentence; Month 2 measures the effect |
| Chunk per page | Exact page numbers for citations | Content spanning pages is split |
| Normalized embeddings + `IndexFlatIP` | Inner product equals cosine; exact search | Not scalable to millions of chunks (not needed here) |
| Page-level match for Recall@k | Comparable across different chunk sizes | Coarser than passage-level matching |
| Evidence threshold on top-1 score | Cheap guard against unsupported answers | A single threshold is crude; it needs tuning |
| Prompt restricts to context and requires citations | Reduces hallucination | Does not eliminate it; Month 3 tests this |

## Limitations
- Scanned or image-only PDFs are not supported (no OCR).
- Retrieval is dense only; no keyword search or reranking.
- The evidence threshold depends on the document set and needs tuning.
- Citation parsing checks that cited numbers exist, not that the claim is truly supported.
- The evaluation set will be small and written by one person.
- No evaluation results are included until experiments are run.

## Roadmap
| Month | Scope | Status |
|---|---|---|
| 1 | PDF ingestion, chunking, embeddings, FAISS, retrieval, LLM answer, sources | Code done; not yet run on real PDFs |
| 2 | Chunk/overlap/k experiments, citation handling, no-evidence handling, verified question set | Code done; questions and experiments not yet run |
| 3 | Streamlit UI, Recall@k reporting, answer-relevance and citation tests, error handling | Not started |
| 4 | Bug fixes, documentation, demo, interview preparation | Not started |
