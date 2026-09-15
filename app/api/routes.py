import time
from fastapi import APIRouter
from app.schemas import QueryRequest
from app.security import validate_sql
from app.analyzer import analyze_query
from app.optimizer import optimize
from app.tools import get_schema, compare_queries
from app.database import execute_read_only

router = APIRouter(prefix="/api/v1")

@router.post("/validate")
def validate(request: QueryRequest):
    return validate_sql(request.sql)

@router.post("/analyze")
def analyze(request: QueryRequest):
    started = time.perf_counter()
    result = analyze_query(request.sql)
    result.warnings.append(f"Analysis latency: {(time.perf_counter() - started) * 1000:.1f} ms")
    return result

@router.post("/optimize")
def optimize_query(request: QueryRequest):
    return optimize(request.sql)

@router.post("/compare")
def compare(request: dict):
    return compare_queries(request.get("original_sql", ""), request.get("optimized_sql", ""))

@router.post("/execute")
def execute(request: QueryRequest):
    return execute_read_only(request.sql)

@router.get("/schema")
def schema():
    return get_schema()
