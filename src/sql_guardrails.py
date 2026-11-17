"""Safety checks before executing generated SQL."""
import re

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|attach|pragma)\b",
    re.I,
)


class UnsafeQueryError(ValueError):
    pass


def ensure_read_only(sql: str) -> str:
    cleaned = sql.strip().rstrip(";")
    if not cleaned.lower().startswith(("select", "with")):
        raise UnsafeQueryError("only SELECT/CTE queries are allowed")
    if FORBIDDEN.search(cleaned):
        raise UnsafeQueryError("write operations are not permitted")
    return cleaned
