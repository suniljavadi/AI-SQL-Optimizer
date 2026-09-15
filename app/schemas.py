from typing import Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    sql: str = Field(min_length=1, max_length=20000)

class Finding(BaseModel):
    category: str
    severity: str
    problem: str
    why_it_matters: str
    recommended_change: str
    expected_benefit: str
    trade_off: str

class Analysis(BaseModel):
    dialect: str = "postgres"
    tables: list[str] = []
    findings: list[Finding] = []
    structure: dict[str, Any] = {}
    warnings: list[str] = []

class OptimizationResponse(BaseModel):
    original_sql: str
    optimized_sql: str
    analysis: Analysis
    indexes: list[str] = []
    explanation: list[Finding] = []
    estimated_improvement: str
    theoretical: bool = True
