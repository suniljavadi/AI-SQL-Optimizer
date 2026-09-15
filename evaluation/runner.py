import json
from pathlib import Path
from app.analyzer import analyze_query

def evaluate(path: str = "evaluation/examples.json") -> dict:
    examples = json.loads(Path(path).read_text(encoding="utf-8"))
    detected = 0
    expected = 0
    for example in examples:
        actual = {finding.category for finding in analyze_query(example["sql"]).findings}
        expected_categories = set(example["expected"])
        detected += len(actual & expected_categories)
        expected += len(expected_categories)
    return {"examples": len(examples), "issue_detection_accuracy": detected / expected if expected else 1.0, "sql_validity": "validated by parser tests", "semantic_equivalence": "requires execution comparison", "hallucination_rate": "not measured without labeled corpus"}

if __name__ == "__main__":
    print(evaluate())
