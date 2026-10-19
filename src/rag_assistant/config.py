import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "data" / "pdfs"
INDEX_DIR = ROOT / "index"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
CHUNK_SIZE = 800     # characters (Month 2: experiment)
CHUNK_OVERLAP = 150  # characters
TOP_K = 4
MIN_SCORE = 0.30     # Month 2: evidence threshold on top-1 cosine score. A STARTING GUESS, tune it with scripts/run_experiments.py output
NO_EVIDENCE_MSG = "I could not find enough evidence in the provided documents to answer this question."
EVAL_FILE = ROOT / "data" / "eval" / "questions.json"
RESULTS_DIR = ROOT / "results"
