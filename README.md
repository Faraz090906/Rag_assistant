# Modular RAG Assistant for Technical PDFs

A modular, command-line Retrieval-Augmented Generation (RAG) assistant that answers questions from technical PDF documents using semantic search, evidence-based answer generation, and source citations. The system includes a configurable retrieval pipeline and a guard that declines to answer when retrieved evidence appears insufficient.

## Project Status

**Current stage: End of Month 2 of a four-month development plan.**

The core implementation for Months 1 and 2 is written, and unit tests covering pure-logic components pass. However, the complete pipeline—including embedding generation, FAISS indexing, retrieval over real PDFs, and LLM-based answer generation—has not yet been validated end to end. Retrieval experiments have also not been run.

Consequently, **no experimental results or performance claims are reported yet**. Results, plots, and configuration decisions will be added only after the corresponding experiments have been executed and verified.

| Component | Current status |
|---|---|
| PDF text extraction and page metadata | Implemented in code |
| Text chunking and metadata preservation | Implemented in code |
| Embedding and FAISS integration | Implemented in code; end-to-end validation pending |
| Retrieval and evidence-threshold logic | Implemented in code; real-document validation pending |
| LLM answer generation and citation handling | Implemented in code; end-to-end validation pending |
| Unit tests for pure-logic components | Passing |
| Retrieval evaluation dataset | Template provided; verified questions still needed |
| Retrieval experiments | Not yet run |
| User interface and final evaluation | Planned for Month 3 |

These statuses distinguish code written from components tested in a real workflow.

> **Project status (read this first):** Months 1 and 2 are *implemented in code*. Unit tests for the pure-logic parts pass. The full pipeline (embeddings, FAISS, LLM) and the retrieval experiments have **not yet been run on real PDFs**, so this repository contains **no experimental results yet**. Results will be added to `results/` and this README only after they are actually produced. See [PROGRESS.md](PROGRESS.md).

## 1. Project Overview

Technical documents often contain information distributed across multiple pages, making manual searching time-consuming. A conventional language model may also generate plausible answers that are not supported by the document being queried.

This project explores how Retrieval-Augmented Generation can make technical document question-answering more useful by retrieving relevant passages before generating a response.

The assistant follows a simple workflow:

1. Extract text from technical PDFs while retaining document names and page numbers.
2. Split the extracted text into overlapping chunks.
3. Convert chunks into embeddings and store them in a FAISS vector index.
4. Retrieve the most relevant chunks for a user's question.
5. Check whether the best retrieval score meets a configurable evidence threshold.
6. Generate an answer using the retrieved context when the threshold is met.
7. Display source references and flag citations that refer to nonexistent sources.

If the evidence threshold is not met, the assistant declines to answer rather than making an unnecessary LLM call.

The evidence threshold is a heuristic, not a guarantee that an answer is correct. Its usefulness must be evaluated on the selected document collection.

## 2. Objectives

The main objectives are to:

- Build a modular RAG pipeline for technical PDF question-answering.
- Preserve document and page metadata throughout ingestion, retrieval, and citation.
- Investigate the effects of chunk size, overlap, and retrieval depth on retrieval quality.
- Implement a configurable guard for questions with insufficient retrieved evidence.
- Evaluate retrieval using manually verified source passages.
- Examine citation validity and the limitations of context-grounded generation.
- Develop a reproducible and understandable implementation suitable for further experimentation.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language and pipeline implementation |
| PyMuPDF | PDF text extraction and page-level processing |
| sentence-transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Default sentence embedding model |
| FAISS | Vector indexing and similarity search |
| Anthropic API | LLM-based answer generation |
| pytest | Unit testing |
| JSON and CSV | Evaluation data and experiment outputs |
| Git and GitHub | Version control and project documentation |

The implementation uses normalized embeddings with FAISS's inner-product index. For normalized vectors, inner product corresponds to cosine similarity.

The project intentionally uses a relatively simple architecture so that individual components can be tested and their behavior understood.

## 4. System Architecture

```text
                  Technical PDF Documents
                            |
                            v
                    PDF Text Extraction
                     (ingest.py)
                            |
                            v
                     Text Chunking
                    (chunking.py)
                            |
                            v
                   Embedding Generation
                   (embeddings.py)
                            |
                            v
                     FAISS Index
                  (vector_store.py)
                            |
                            v
User Question --> Query Embedding --> Top-k Retrieval
                            |         (retriever.py)
                            v
                   Evidence Threshold
                    (evidence.py)
                      /         \
              Insufficient      Sufficient
                evidence        evidence
                   |                |
                   v                v
             Decline to        LLM Generation
                answer         (generator.py)
                                    |
                                    v
                            Citation Processing
                              (citations.py)
                                    |
                                    v
                             Final Response
                         + Source References
```

The `pipeline.py` module coordinates these components, while the scripts in `scripts/` provide commands for indexing documents, asking questions, and running retrieval experiments.

## 5. Repository Structure

```text
rag-assistant/
├── README.md
├── PROGRESS.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   ├── pdfs/
│   └── eval/
│       ├── questions.example.json
│       └── questions.json
│
├── src/
│   └── rag_assistant/
│       ├── config.py
│       ├── ingest.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── evidence.py
│       ├── generator.py
│       ├── citations.py
│       ├── metrics.py
│       └── pipeline.py
│
├── scripts/
│   ├── build_index.py
│   ├── ask.py
│   └── run_experiments.py
│
├── tests/
│
└── results/
```

**Directory responsibilities**

- `data/pdfs/`: local technical PDFs; documents are excluded from version control by default.
- `data/eval/`: evaluation-question templates and manually verified questions.
- `src/rag_assistant/`: reusable ingestion, retrieval, generation, and evaluation logic.
- `scripts/`: command-line entry points for building the index, asking questions, and running experiments.
- `tests/`: unit tests and, as development progresses, integration tests.
- `results/`: experiment outputs generated by actual runs.

The exact contents of each directory should match the current repository. Do not create empty or placeholder modules merely to make the tree look complete.

## 6. Installation and Setup

### Prerequisites

- Python version compatible with the installed dependencies.
- pip and a virtual environment.
- Technical PDFs containing selectable text.
- An Anthropic API key for LLM-based answer generation. Retrieval can be tested separately without an API key if the implementation supports retrieval-only mode.

### Clone the repository

```bash
git clone <your-repository-url>
cd rag-assistant
```

Replace the placeholder with your actual repository URL.

### Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Linux or macOS**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Configure environment variables

Copy `.env.example` to `.env` and configure the required variables.

For example:

```dotenv
ANTHROPIC_API_KEY=your_api_key_here
```

The actual variable names must match those read by `config.py`. If the project reads environment variables directly, export them in your shell instead. If it loads `.env` automatically, ensure the required environment-loading dependency is installed.

Never commit `.env` or expose a real API key in source code, screenshots, logs, or GitHub.

The first embedding-model download requires an internet connection and may take some time.

### Add documents

Place suitable technical PDFs in:

```text
data/pdfs/
```

Start with a small collection of documents whose content and page numbers can be checked manually.

Scanned, image-only PDFs are not supported by the current text-extraction pipeline unless OCR is added.

## 7. Running the Application

### Build the index

```bash
python scripts/build_index.py
```

This command should extract the document text, create chunks and embeddings, and build the FAISS index.

Check the script's actual configuration for the index output location and ensure the documents were processed successfully.

### Ask questions

```bash
python scripts/ask.py
```

Ask questions whose answers can be located in the uploaded documents. Verify the cited pages manually rather than assuming that a generated citation proves correctness.

If retrieval-only mode is supported, test that mode before configuring the LLM API. This helps separate retrieval problems from generation problems.

### Run unit tests

```bash
pytest -q
```

The pure-logic unit tests currently pass. A successful unit-test run does not, by itself, establish that the complete embedding, FAISS, and LLM pipeline works correctly.

### Run retrieval experiments

After creating and verifying the evaluation questions:

```bash
python scripts/run_experiments.py
```

The experiment script is intended to write:

```text
results/retrieval_experiments.csv
```

Run this command against the actual implementation before reporting any results. If the script fails, record the issue and fix it rather than inventing an output file.

## 8. Retrieval and Answering Pipeline

### 8.1 PDF ingestion

The ingestion module extracts text page by page and records metadata such as source filename and page number.

Page-level metadata is retained so retrieved passages can be traced back to their original locations.

### 8.2 Chunking

Extracted page text is divided into fixed-size character chunks with configurable overlap.

The overlap helps preserve context near chunk boundaries. However, fixed-size character chunking can split sentences, equations, tables, and technical definitions.

The current design favors simplicity and predictable behavior. More advanced chunking methods can be considered if the experiments justify them.

### 8.3 Embeddings and vector search

The default embedding model is:

`sentence-transformers/all-MiniLM-L6-v2`

The model converts each chunk into a vector representation. The vectors are normalized before being indexed with FAISS.

The index uses exact inner-product search, which is suitable for a relatively small document collection and avoids introducing approximate-search behavior into the initial experiments.

### 8.4 Retrieval

For each question, the retriever returns the top-k chunks according to similarity.

The `top-k` parameter controls how many passages are supplied to the subsequent evidence check and generation stage.

A larger k may improve coverage but can also introduce irrelevant context. This trade-off will be investigated experimentally.

### 8.5 Evidence threshold

The evidence module compares the best retrieval score against a configurable threshold, `MIN_SCORE`.

If the score is below the threshold, the system declines to answer. Otherwise, the retrieved passages are passed to the LLM.

The default threshold of `0.30` is an initial configuration, not an experimentally established optimum. The appropriate value depends on the embedding model, documents, question types, and retrieval implementation.

A high similarity score also does not guarantee that the retrieved passage answers the question. This limitation is important when interpreting the assistant's responses.

### 8.6 Answer generation

The generator uses the Anthropic API to answer questions from the retrieved context.

The prompt instructs the model to:
- Use the supplied evidence rather than unsupported external knowledge.
- State when the context does not contain enough information.
- Cite relevant passages using numbered references such as `[1]`.
- Avoid inventing document content or source references.

Prompt instructions can reduce unsupported answers but cannot eliminate hallucinations.

### 8.7 Citation handling

The citation module parses numbered citations in the answer and checks whether the referenced source numbers exist.

It also identifies which retrieved sources were cited and flags references that do not correspond to available sources.

This is a citation-validity check, not a full verification that every claim is entailed by the cited passage. Semantic citation verification remains a potential extension.

## 9. Evaluation Methodology

The project uses a manually verified evaluation set rather than relying solely on a few demonstration questions.

### Evaluation dataset

Create approximately 15–25 questions initially, including:
- Direct factual questions answered by a single passage.
- Questions requiring information from multiple passages.
- Questions involving technical definitions or explanations.
- Questions whose answers are not present in the documents.

For answerable questions, record the expected answer and the relevant source file and page or pages. For unanswerable questions, verify that the required information is genuinely absent from the selected collection.

The question set should be created and checked against the actual documents before experiments are run.

### Retrieval experiments

The planned experiment script compares the following configurations:

| Parameter | Planned values |
|---|---|
| Chunk size | 400, 800, 1200 characters |
| Chunk overlap | 0, 100, 200 characters |
| Retrieval depth (k) | 1, 2, 4, 6 |

Not every parameter combination is necessarily optimal. The script should validate configurations and report errors for invalid combinations, such as an overlap that is not smaller than the chunk size.

### Metrics

**Recall@k**

Measures whether at least one relevant source passage appears in the top-k retrieved results, based on the relevance labels in the evaluation dataset.

**Mean Reciprocal Rank (MRR)**

Measures how highly the first relevant result appears in the ranked retrieval results. For a query with first relevant result at rank r, its reciprocal rank is 1/r; MRR averages this value over the evaluated queries.

**Top-1 score analysis**

Compare the best retrieval scores for answerable and unanswerable questions. This helps investigate whether a similarity threshold can separate some unsupported questions from questions with relevant evidence.

A score gap is evidence about the tested dataset, not proof that the threshold will generalize to other documents or users.

### Selecting the evidence threshold

The default `MIN_SCORE = 0.30` should be treated as a starting value.

Use the evaluation set to examine:
- How often answerable questions are declined.
- How often unanswerable questions pass the threshold.
- How these outcomes change as the threshold changes.

Select a threshold based on the observed trade-off and document the rationale. Avoid tuning and reporting results on exactly the same small set as if it were an independent test set.

### Planned result artifacts

Once the experiments have actually run, add:
- `results/retrieval_experiments.csv`
- A concise summary of the best-performing configurations.
- A comparison of retrieval settings.
- An analysis of answerable versus unanswerable top-1 scores.
- The selected threshold and its limitations.

No values should be reported until the corresponding experiment outputs have been produced and checked.

## 10. Testing Strategy

The testing approach is divided into three levels.

**Unit tests**

Test pure-logic components such as chunking, metadata handling, evidence-threshold decisions, citation parsing, and metric calculations.

**Integration tests**

As the project develops, add tests that connect PDF extraction, chunking, retrieval, and answer orchestration. External API calls can be mocked where appropriate to make tests reproducible.

**End-to-end validation**

Run the full pipeline on real technical PDFs. Confirm that documents are indexed, queries return meaningful passages, citations refer to the correct pages, and the evidence guard behaves as intended.

A mocked LLM response is useful for testing application logic, but it is not evidence that live LLM generation works correctly.

## 11. Design Decisions and Trade-offs

| Design choice | Reason | Limitation |
|---|---|---|
| Fixed-size character chunks | Simple to implement and compare | May split sentences or technical expressions |
| Page-level metadata | Makes page citations possible | Information spanning pages can be fragmented |
| Normalized embeddings with `IndexFlatIP` | Exact vector search using inner product | Memory and search costs increase with corpus size |
| Dense retrieval only | Keeps the initial architecture manageable | May miss exact identifiers, symbols, or uncommon terminology |
| Top-1 evidence threshold | Simple mechanism for declining low-confidence retrievals | A single score does not reliably measure answerability |
| Context-restricted prompt | Encourages evidence-grounded generation | Does not guarantee factual correctness |
| Numbered citation validation | Detects nonexistent citation references | Does not establish semantic support for every claim |
| Small manually verified dataset | Feasible for a student project | Limited coverage and potential annotation bias |

These choices prioritize a transparent baseline that can be evaluated and improved without making the initial implementation unnecessarily complex.

## 12. Limitations

The current design has several known limitations:

- Scanned or image-only PDFs are unsupported without OCR.
- Dense retrieval may be less effective for exact identifiers, equations, and unusual technical terminology.
- Fixed-size character chunks may split meaningful content.
- The evidence threshold is heuristic and requires evaluation.
- Valid citation numbering does not prove that the cited source supports the associated claim.
- A small evaluation set may not represent the full range of technical questions.
- LLM outputs can still contain unsupported or incorrect information.
- API availability, latency, and cost may affect answer generation.
- The current exact vector-search approach is intended for a small collection, not a massive document corpus.
- The complete pipeline and retrieval experiments have not yet been validated on real PDFs.

These limitations define the scope of the current project and provide clear directions for future work.

## 13. Development Roadmap

The project is organized as a four-month student development plan.

| Month | Planned scope | Status |
|---|---|---|
| 1 | PDF ingestion, chunking, embeddings, FAISS indexing, retrieval, and basic answer generation | Core code implemented; end-to-end validation pending |
| 2 | Retrieval configuration experiments, citation handling, evidence-threshold logic, and evaluation-question preparation | Code implemented; verified questions and experiments pending |
| 3 | Basic Streamlit interface, retrieval evaluation, answer and citation checks, error handling, and integration testing | Not started |
| 4 | Bug fixes, final evaluation, documentation, demo, and interview preparation | Not started |

The timeline records development stages, not a claim that every feature has already been validated. Update the status column as work is actually completed.

## 14. Future Improvements

Potential extensions, depending on the evaluation findings and available time, include:

- Comparing character-based chunking with sentence-aware chunking.
- Adding keyword retrieval for exact technical terms.
- Combining lexical and dense retrieval.
- Improving handling of questions that require multiple passages.
- Adding OCR support for scanned documents.
- Evaluating citation support beyond checking citation numbers.
- Caching embeddings and reusing indexes to reduce repeated work.
- Comparing alternative embedding models.
- Adding a small interface for document upload, question-answering, and source inspection.

These are possible extensions rather than features claimed to exist in the current implementation.

## 15. Security and Responsible Use

- Store API keys in environment variables and exclude local secrets from version control.
- Use documents that you are permitted to process and share.
- Avoid uploading confidential documents to an external LLM provider without authorization.
- Treat PDF contents as untrusted input; instructions embedded in documents should not override the application's system instructions.
- Do not treat generated answers as authoritative without checking the cited evidence.
- Clearly distinguish retrieval confidence from answer correctness.

## 16. Learning Outcomes

The project is intended to develop practical understanding of:

- The RAG architecture and the separation between retrieval and generation.
- Text preprocessing, chunking, and embedding-based semantic search.
- Vector indexing and similarity measures.
- Evidence thresholds and their limitations.
- Citation metadata and source traceability.
- Retrieval evaluation using Recall@k and MRR.
- Reproducible experiments and modular Python design.
- Testing, error handling, and responsible use of external LLM APIs.

The final learning outcomes and experimental conclusions should be updated after implementation and evaluation.

## 17. Conclusion

This project establishes a modular baseline for question-answering over technical PDFs. Rather than assuming that an LLM can reliably answer every question, it combines semantic retrieval, source metadata, a configurable evidence guard, and numbered citations.

The next stage is to validate the complete pipeline on real documents, run the planned retrieval experiments, and use the findings to guide improvements. The objective is not simply to produce answers, but to understand when retrieval works, when it fails, and how those failures can be measured and communicated.

---

**Current status:** Core code for the first two development stages is written, and pure-logic unit tests pass. Full-pipeline validation and retrieval experiments remain pending. No experimental performance results are claimed at this stage.