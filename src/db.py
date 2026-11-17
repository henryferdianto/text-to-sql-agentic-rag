"""Create a small SQLite warehouse for the demo agent."""
import sqlite3
from pathlib import Path

DEFAULT = Path("data/warehouse.db")


def build(path: Path = DEFAULT) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript(
        """
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;
        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, segment TEXT);
        CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, created_at TEXT);
        """
    )
    con.executemany(
        "INSERT INTO customers VALUES (?,?,?)",
        [(1, "Ani", "retail"), (2, "Budi", "enterprise"), (3, "Citra", "retail")],
    )
    con.executemany(
        "INSERT INTO orders VALUES (?,?,?,?)",
        [
            (1, 1, 150000, "2026-01-03"),
            (2, 2, 900000, "2026-01-05"),
            (3, 1, 200000, "2026-02-11"),
            (4, 3, 50000, "2026-02-20"),
        ],
    )
    con.commit()
    con.close()
    return path


if __name__ == "__main__":
    print("warehouse ->", build())
