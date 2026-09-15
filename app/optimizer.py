import re
from app.analyzer import analyze_query
from app.schemas import OptimizationResponse

def generate_optimized_sql(sql: str) -> str:
    return re.sub(r"YEAR\s*\(\s*([\w.]+)\s*\)\s*=\s*(\d{4})", lambda match: f"{match.group(1)} >= '{match.group(2)}-01-01' AND {match.group(1)} < '{int(match.group(2)) + 1}-01-01'", sql, flags=re.I)

def optimize(sql: str) -> OptimizationResponse:
    analysis = analyze_query(sql)
    optimized = generate_optimized_sql(sql)
    indexes = []
    if any(f.category == "sargability" for f in analysis.findings):
        indexes.append("CREATE INDEX ix_orders_order_date ON orders(order_date); -- verify it does not already exist")
    if "orders" in analysis.tables:
        indexes.append("CREATE INDEX ix_orders_customer_id ON orders(customer_id); -- justify with join selectivity and write volume")
    return OptimizationResponse(original_sql=sql, optimized_sql=optimized, analysis=analysis, indexes=indexes, explanation=analysis.findings, estimated_improvement="Potentially lower rows scanned; measure with EXPLAIN ANALYZE on synthetic data.")
