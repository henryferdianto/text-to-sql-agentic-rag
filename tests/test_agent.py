import pytest

from src.agent import answer_question
from src.db import build
from src.sql_guardrails import UnsafeQueryError, ensure_read_only


@pytest.fixture()
def warehouse(tmp_path):
    return build(tmp_path / "warehouse.db")


def test_guardrails_allow_select():
    assert ensure_read_only("SELECT 1") == "SELECT 1"


@pytest.mark.parametrize("sql", ["DROP TABLE orders", "SELECT 1; DROP TABLE orders", "PRAGMA x"])
def test_guardrails_block_writes(sql):
    with pytest.raises(UnsafeQueryError):
        ensure_read_only(sql)


def test_answer_question_total_revenue(warehouse):
    answer = answer_question("What is the total revenue?", warehouse)
    assert answer.rows[0]["total_revenue"] == 1_300_000


def test_answer_question_count(warehouse):
    answer = answer_question("How many orders?", warehouse)
    assert answer.rows[0]["n_orders"] == 4
