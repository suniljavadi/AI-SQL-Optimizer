from app.analyzer import parse_sql, analyze_query
from app.optimizer import generate_optimized_sql
from app.security import validate_sql
from app.rules import search_optimization_rules

def get_schema() -> dict:
    return {"tables": {"customers": ["customer_id", "name", "region", "created_at"], "orders": ["order_id", "customer_id", "order_date", "total_amount", "status"]}}

def get_indexes() -> list[str]:
    return ["ix_orders_customer_id(customer_id)", "ix_orders_order_date(order_date)"]

def compare_queries(original: str, optimized: str) -> dict:
    return {"original": original, "optimized": optimized, "theoretical": True, "message": "Execution statistics are unavailable until both queries run against the local synthetic database."}
