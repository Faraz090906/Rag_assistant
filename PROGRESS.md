# Progress Log

Start date: <fill in real date>. Nothing existed before this project began.

## Status
| Month | Item | State |
|---|---|---|
| 1 | Ingest, chunk, embed, FAISS, retrieve, LLM answer, sources | Code written |
| 1 | Run on real PDFs | **Not done** |
| 2 | Evidence check, citation validation, metrics, experiment script | Code written |
| 2 | Verified question set | **Not done (you must write and verify it)** |
| 2 | Run experiments, compare configurations | **Not done** |
| 3 | Streamlit UI, evaluation of answers, error handling | Not started |
| 4 | Cleanup, docs, demo, interview prep | Not started |

## What is verified
- 8 unit tests pass (chunking, prompt, evidence threshold, citation parsing, Recall@k, MRR), run in a sandbox without network.
- All modules compile.

## What is NOT verified
- Embedding, FAISS and LLM calls on real PDFs.
- Any retrieval quality number. None exist yet.
- The default `MIN_SCORE = 0.30`: an untested guess.

## Your checklist
- [ ] Install requirements; add 3-5 text-based PDFs
- [ ] `python scripts/build_index.py`; record pages and chunks
- [ ] `python scripts/ask.py` with 5 questions; note relevance of sources
- [ ] Write and verify `data/eval/questions.json`
- [ ] `python scripts/run_experiments.py`; commit `results/retrieval_experiments.csv`
- [ ] Choose `MIN_SCORE` from the data and record why
- [ ] Run `pytest`

## Dated log (fill in as you go)
| Date | What I did | Real observation |
|---|---|---|
| | | |

## Remaining
Months 3 and 4 plus the unchecked items above. Realistic timeline: finish the checklist, then start Month 3 once real results exist.
