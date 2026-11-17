"""A deterministic text-to-SQL analyst used for offline demos.

The rule-based planner keeps the repository runnable without an LLM; swap
`generate_sql` for an LLM call to enable open-ended questions.
"""
from dataclasses import dataclass
import re
import sqlite3

from src.db import DEFAULT, build
from src.sql_guardrails import ensure_read_only

SCHEMA = "customers(id, name, segment) / orders(id, customer_id, amount, created_at)"

RULES = [
    (r"total (revenue|sales)", "SELECT ROUND(SUM(amount), 2) AS total_revenue FROM orders"),
    (r"(how many|number|count) (of )?(orders|transactions)", "SELECT COUNT(*) AS n_orders FROM orders"),
    (r"top customers?.*(revenue|spend)", """
        SELECT c.name, ROUND(SUM(o.amount), 2) AS revenue
        FROM orders o JOIN customers c ON c.id = o.customer_id
        GROUP BY c.name ORDER BY revenue DESC LIMIT 5
    """),
    (r"(revenue|sales).*(segment|per segment)", """
        SELECT c.segment, ROUND(SUM(o.amount), 2) AS revenue
        FROM orders o JOIN customers c ON c.id = o.customer_id
        GROUP BY c.segment ORDER BY revenue DESC
    """),
]


@dataclass
class Answer:
    sql: str
    rows: list[dict]


def generate_sql(question: str) -> str:
    q = question.lower()
    for pattern, sql in RULES:
        if re.search(pattern, q):
            return " ".join(sql.split())
    return "SELECT COUNT(*) AS rows_in_orders FROM orders"


def repair_sql(question: str, failed_sql: str) -> str:
    return "SELECT COUNT(*) AS rows_in_orders FROM orders"


def answer_question(question: str, db_path=DEFAULT) -> Answer:
    if not __import__("pathlib").Path(db_path).exists():
        build(__import__("pathlib").Path(db_path))
    sql = ensure_read_only(generate_sql(question))
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    try:
        for _ in range(2):
            try:
                rows = [dict(r) for r in con.execute(sql).fetchall()]
                return Answer(sql=sql, rows=rows)
            except sqlite3.Error:
                sql = ensure_read_only(repair_sql(question, sql))
        raise
    finally:
        con.close()
