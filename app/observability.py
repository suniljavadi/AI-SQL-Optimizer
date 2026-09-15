import hashlib
import logging
import time

logger = logging.getLogger("ai_sql_optimizer")

def query_fingerprint(sql: str) -> str:
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()[:16]

def record_event(event: str, sql: str, latency_ms: float, error: str | None = None) -> None:
    logger.info("event=%s query_id=%s latency_ms=%.1f error=%s", event, query_fingerprint(sql), latency_ms, bool(error))

class Timer:
    def __enter__(self):
        self.started = time.perf_counter()
        return self
    def __exit__(self, *_):
        self.elapsed_ms = (time.perf_counter() - self.started) * 1000
