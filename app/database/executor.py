import time
from sqlalchemy import create_engine, text
from app.config import settings
from app.security import validate_sql

def execute_read_only(sql: str, database_url: str | None = None, row_limit: int | None = None) -> dict:
    validation = validate_sql(sql)
    if not validation["valid"]:
        return {"executed": False, "errors": validation["errors"], "theoretical": True}
    limit = row_limit or settings.max_rows
    statement = f"SELECT * FROM ({validation['normalized_sql']}) AS safe_query LIMIT {int(limit)}"
    started = time.perf_counter()
    try:
        engine = create_engine(database_url or settings.database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            rows = [dict(row._mapping) for row in connection.execute(text(statement))]
        return {"executed": True, "rows": rows, "row_count": len(rows), "execution_ms": (time.perf_counter() - started) * 1000, "theoretical": False}
    except Exception as error:
        return {"executed": False, "errors": [str(error)], "theoretical": True}
