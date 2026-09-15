import re
import sqlglot
from sqlglot import exp

DANGEROUS = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|EXEC(?:UTE)?|MERGE|COPY)\b", re.I)

def validate_sql(sql: str) -> dict:
    text = sql.strip().rstrip(';').strip()
    if not text:
        return {"valid": False, "errors": ["SQL is empty."], "normalized_sql": ""}
    if DANGEROUS.search(text):
        return {"valid": False, "errors": ["Only read-only SELECT statements are allowed."], "normalized_sql": ""}
    try:
        parsed = sqlglot.parse_one(text, read="postgres")
        if not isinstance(parsed, (exp.Select, exp.Union, exp.With)) and not parsed.find(exp.Select):
            return {"valid": False, "errors": ["Statement must contain a SELECT query."], "normalized_sql": ""}
        return {"valid": True, "errors": [], "normalized_sql": parsed.sql(dialect="postgres")}
    except Exception as error:
        return {"valid": False, "errors": [f"SQL parse error: {error}"], "normalized_sql": ""}
