# RAG Chunking & Retrieval Comparison

> **Work in progress.** This README is a placeholder and will be rewritten once the project is complete. Results are not available yet.

A from-scratch comparison of chunking strategies and retrieval methods for retrieval-augmented generation (RAG) over arXiv ML/CS papers. The goal is to measure how the way documents are split, and the way chunks are retrieved and reranked, affects retrieval quality.

## Plan

**Chunking methods** (each implemented from scratch, no LangChain splitters)

| Method | Idea | Status |
|---|---|---|
| Fixed-size | Cut every N characters with overlap; the naive baseline | Done |
| Recursive | Split on the largest natural boundary first (paragraph, line, sentence, word), merge small pieces back up to the size limit, with overlap | Done |
| Section-aware | Use the paper's own headings as chunk boundaries, detected from font size and weight | In progress |
| Semantic | Split where embedding similarity between consecutive sentences drops | Planned |

**Retrieval methods**

| Method | Status |
|---|---|
| BM25 (sparse) | Planned |
| Dense embeddings (`BAAI/bge-small-en-v1.5` + FAISS) | Planned |
| Hybrid (BM25 + dense, reciprocal rank fusion) | Planned |
| Hybrid + cross-encoder reranking | Planned |

**Evaluation**

- 4 chunking methods x 4 retrieval methods = 16 combinations
- Metrics: hit rate@k and MRR, computed against a hand-verified question set
- Ground-truth QA set (`data/qa_set.json`): in progress

## Corpus

15 arXiv ML/CS papers, by arXiv ID:

2606.30774, 2606.30840, 2606.30846, 2606.30850, 2606.30852, 2606.30863, 2606.30906, 2606.30911, 2606.30931, 2606.30949, 2606.30953, 2606.30966, 2606.30970, 2606.30975, 2606.30997

## Repository structure

```
.
├── data/
│   ├── papers/             # source PDFs
│   └── qa_set.json         # ground-truth questions
├── src/
│   ├── extract.py          # PDF -> text (PyMuPDF, column-aware reading order)
│   ├── chunking/
│   │   ├── Fixed.py
│   │   ├── Recursive.py
│   │   ├── section_aware.py
│   │   └── semantic.py
│   ├── retrieval/
│   └── evaluate.py
├── results/
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the PDFs in `data/papers/`, then extract their text:

```bash
python src/extract.py
```

Each chunker can be run on its own to see a demo on a short test string:

```bash
python src/chunking/Fixed.py
python src/chunking/Recursive.py
```

## Design notes

- **Characters as the unit.** Chunk sizes are measured in characters for all methods, so the comparison is about strategy, not tokenizer choice.
- **Two-column layouts.** Text extraction sorts blocks by position so that left and right columns are not interleaved.
- **Known limitation (recursive chunker).** Overlap is not carried across a boundary where a piece had to be re-split recursively.
