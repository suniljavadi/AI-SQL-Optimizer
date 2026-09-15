from fastapi.testclient import TestClient
from app.main import app
from app.analyzer import analyze_query
from app.optimizer import generate_optimized_sql
from app.rules import search_optimization_rules
from app.security import validate_sql

client = TestClient(app)

def test_parser_and_date_analysis():
    analysis = analyze_query("SELECT * FROM orders WHERE YEAR(order_date) = 2026")
    assert "orders" in analysis.tables
    assert any(f.category == "sargability" for f in analysis.findings)

def test_safe_rewrite():
    result = generate_optimized_sql("SELECT * FROM orders WHERE YEAR(order_date) = 2026")
    assert "order_date >= '2026-01-01'" in result
    assert "order_date < '2027-01-01'" in result

def test_dangerous_sql_blocked():
    assert validate_sql("DROP TABLE orders")["valid"] is False
    assert validate_sql("SELECT * FROM orders")["valid"] is True

def test_rag_returns_relevant_rule():
    assert search_optimization_rules("date index sargability")

def test_api_endpoints():
    assert client.get("/health").status_code == 200
    assert client.get("/api/v1/schema").json()["tables"]["orders"]
    assert client.post("/api/v1/validate", json={"sql": "SELECT 1"}).json()["valid"]
    assert client.post("/api/v1/optimize", json={"sql": "SELECT * FROM orders"}).status_code == 200
    assert client.post("/api/v1/execute", json={"sql": "DROP TABLE orders"}).json()["executed"] is False
