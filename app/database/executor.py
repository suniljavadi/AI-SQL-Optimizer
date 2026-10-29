import logging
import time
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import settings
from app.observability import record_event
from app.security import validate_sql


logger = logging.getLogger(__name__)


@lru_cache(maxsize=4)
def _get_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def execute_read_only(
    sql: str,
    database_url: str | None = None,
    row_limit: int | None = None,
) -> dict:
    validation = validate_sql(sql)
    if not validation["valid"]:
        return {"executed": False, "errors": validation["errors"], "theoretical": True}
    requested_limit = settings.max_rows if row_limit is None else row_limit
    if requested_limit < 1:
        return {
            "executed": False,
            "errors": ["Row limit must be positive."],
            "theoretical": True,
        }
    limit = min(requested_limit, settings.max_rows)
    statement = f"SELECT * FROM ({validation['normalized_sql']}) AS safe_query LIMIT {int(limit)}"
    started = time.perf_counter()
    try:
        engine = _get_engine(database_url or settings.database_url)
        with engine.connect() as connection, connection.begin():
            if connection.dialect.name == "postgresql":
                connection.exec_driver_sql("SET TRANSACTION READ ONLY")
                connection.execute(
                    text("SELECT set_config('statement_timeout', :timeout, true)"),
                    {"timeout": f"{settings.query_timeout_seconds}s"},
                )
            rows = [
                dict(row._mapping)
                for row in connection.execute(text(statement))
            ]
        execution_ms = (time.perf_counter() - started) * 1000
        record_event("query_execution", sql, execution_ms)
        return {
            "executed": True,
            "rows": rows,
            "row_count": len(rows),
            "execution_ms": execution_ms,
            "theoretical": False,
        }
    except Exception as error:
        execution_ms = (time.perf_counter() - started) * 1000
        logger.error("Database query failed (%s)", type(error).__name__)
        record_event("query_execution", sql, execution_ms, type(error).__name__)
        return {
            "executed": False,
            "errors": ["Database execution failed."],
            "theoretical": True,
        }
