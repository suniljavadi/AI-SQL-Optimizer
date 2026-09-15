from app.tools import get_schema, get_indexes
from app.security import validate_sql
from app.analyzer import analyze_query
from app.optimizer import generate_optimized_sql
from app.rules import search_optimization_rules

def optimize_with_tools(sql: str) -> dict:
    validation = validate_sql(sql)
    if not validation["valid"]:
        return {"validation": validation, "error": "Tool chain stopped before optimization."}
    analysis = analyze_query(sql, get_indexes())
    rules = search_optimization_rules(" ".join(f.problem for f in analysis.findings))
    return {"validation": validation, "schema": get_schema(), "indexes": get_indexes(), "analysis": analysis, "rules": rules, "optimized_sql": generate_optimized_sql(sql)}
