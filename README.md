# Autonomous Text-to-SQL & Agentic RAG Data Analyst System

![ci](https://github.com/henryferdianto/text-to-sql-agentic-rag/actions/workflows/ci.yml/badge.svg)

> **Natural-language business questions to self-correcting SQL and cited answers**

## Overview

An autonomous data analyst agent that translates natural-language questions into self-correcting SQL queries and hybrid-search document citations, evaluated with LLM-as-a-judge metrics and served through Streamlit.

## Approach

1. **Intent routing**: decide between structured (SQL) and unstructured (RAG) retrieval.
2. **Text-to-SQL agent**: generate, validate and self-correct SQL against schema.
3. **Hybrid retrieval**: dense + lexical search with document citations.
4. **Evaluation**: RAGAS-style faithfulness and retrieval precision.
5. **Interface**: interactive Streamlit app for real-time querying.

## Repository Structure

```
text-to-sql-agentic-rag/
├── src/
│   ├── agent.py            # LangGraph orchestration
│   ├── retriever.py        # hybrid retrieval
│   └── sql_guardrails.py   # read-only validation
├── app/streamlit_app.py
├── requirements.txt
└── README.md
```

## Tech Stack

`Python` · `LangGraph` · `LangChain` · `SQLAlchemy` · `PostgreSQL/MySQL` · `Streamlit` · `RAGAS`

## Getting Started

```bash
git clone https://github.com/henryferdianto/text-to-sql-agentic-rag.git
cd text-to-sql-agentic-rag
pip install -r requirements.txt
```

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
python -m streamlit run app/streamlit_app.py
```


<!-- completed -->

## Quickstart with Sample Data

The repository ships a synthetic data generator so the full pipeline can be run
without any private dataset:

```bash
python -m src.db && python -m src.run_demo
```

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

## Project Status

This repository contains the project documentation and a runnable reference
implementation. A synthetic data generator is included so every pipeline stage
can be executed end-to-end; replace the sample data with your own datasets in
`data/raw/` to reproduce real results.

## License

MIT License — see [LICENSE](LICENSE).


---

**Author:** Rifky Henry Ferdianto — Data Science undergraduate at ITERA  
GitHub: [@henryferdianto](https://github.com/henryferdianto) · Portfolio: [rifky-henry-ferdianto](https://github.com/henryferdianto/rifky-henry-ferdianto)
