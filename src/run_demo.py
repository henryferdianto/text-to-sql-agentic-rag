from src.agent import answer_question
from src.db import build


def main():
    build()
    for question in (
        "What is the total revenue?",
        "How many orders are there?",
        "Top customers by revenue",
        "Revenue per segment",
    ):
        answer = answer_question(question)
        print(f"Q: {question}\n  SQL: {answer.sql}\n  -> {answer.rows}\n")


if __name__ == "__main__":
    main()
