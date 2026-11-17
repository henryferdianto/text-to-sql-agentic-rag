"""LangGraph-style orchestration skeleton for the data analyst agent."""
from dataclasses import dataclass
from sqlalchemy import create_engine, text
from .sql_guardrails import ensure_read_only


@dataclass
class Answer:
    sql: str
    rows: list[dict]
    citations: list[str]


def answer_question(question: str, database_url: str, docs: list[str]) -> Answer:
    engine = create_engine(database_url)
    sql = generate_sql(question)

    for _ in range(3):  # self-correction loop
        try:
            stmt = ensure_read_only(sql)
            with engine.connect() as conn:
                rows = [dict(r._mapping) for r in conn.execute(text(stmt))]
            return Answer(sql=stmt, rows=rows, citations=docs[:3])
        except Exception:
            sql = repair_sql(question, sql)
    raise RuntimeError("agent could not produce a valid query")


def generate_sql(question: str) -> str:
    # TODO: call your LLM with the database schema as context.
    return "SELECT 1 AS placeholder"


def repair_sql(question: str, failed_sql: str) -> str:
    # TODO: ask the LLM to fix the failing SQL using the error message.
    return failed_sql
