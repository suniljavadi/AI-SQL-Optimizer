RULES = [
    {"id": "sargable-date", "text": "Replace YEAR(date_column)=year with a half-open range to preserve index access and avoid applying a function per row.", "tags": ["date", "sargability", "index"]},
    {"id": "select-list", "text": "Avoid SELECT *; project only columns needed by the consumer to reduce I/O and network transfer.", "tags": ["projection", "select"]},
    {"id": "join-index", "text": "Index foreign-key columns used in joins when cardinality and workload justify the write and storage overhead.", "tags": ["join", "index"]},
    {"id": "sort-index", "text": "An ORDER BY can require a sort; a compatible predicate/order index may avoid it, but verify selectivity and direction.", "tags": ["sort", "index"]},
    {"id": "read-only", "text": "Only execute validated SELECT statements with a row limit and timeout in the synthetic database.", "tags": ["security", "execution"]},
    {"id": "cardinality", "text": "Index recommendations must consider selectivity, existing indexes, cardinality, and write amplification.", "tags": ["index", "cardinality"]},
]

def search_optimization_rules(query: str, limit: int = 5) -> list[dict]:
    tokens = set(query.lower().split())
    scored = [(sum(token in (r["text"] + " " + " ".join(r["tags"])).lower() for token in tokens), r) for r in RULES]
    return [r for score, r in sorted(scored, key=lambda item: item[0], reverse=True)[:limit] if score]
