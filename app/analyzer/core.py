import re
import sqlglot
from sqlglot import exp
from app.schemas import Analysis, Finding

def parse_sql(sql: str):
    return sqlglot.parse_one(sql, read="postgres")

def analyze_query(sql: str, indexes: list[str] | None = None) -> Analysis:
    tree = parse_sql(sql)
    text = sql.upper()
    tables = sorted({table.name for table in tree.find_all(exp.Table)})
    findings: list[Finding] = []
    if re.search(r"SELECT\s+\*", text):
        findings.append(Finding(category="projection", severity="medium", problem="SELECT * returns every column.", why_it_matters="It increases I/O, network transfer, and schema coupling.", recommended_change="Select only columns required by the consumer.", expected_benefit="Lower row width and clearer contracts.", trade_off="Requires maintaining an explicit column list."))
    if not tree.find(exp.Where):
        findings.append(Finding(category="filtering", severity="high", problem="Query has no WHERE clause.", why_it_matters="It may scan and return the entire relation.", recommended_change="Add a selective predicate when the business request permits.", expected_benefit="Less work and fewer rows transferred.", trade_off="An incorrect filter changes results."))
    if re.search(r"YEAR\s*\(", text) or re.search(r"DATE_PART\s*\(", text):
        findings.append(Finding(category="sargability", severity="high", problem="Function applied to a date predicate column.", why_it_matters="The database may need to evaluate the function for every row instead of seeking the date index.", recommended_change="Use a half-open range such as order_date >= '2026-01-01' AND order_date < '2027-01-01'.", expected_benefit="Can enable an index range scan and reduce rows examined.", trade_off="Date boundaries must be correct for the column type and timezone."))
    joins = list(tree.find_all(exp.Join))
    if joins and any(join.args.get("on") is None for join in joins):
        findings.append(Finding(category="join", severity="high", problem="Join without an ON condition may be Cartesian.", why_it_matters="It multiplies rows and can overwhelm memory and CPU.", recommended_change="Add an explicit, validated join predicate.", expected_benefit="Prevents accidental row multiplication.", trade_off="The correct relationship must be known."))
    if tree.find(exp.Order):
        findings.append(Finding(category="sorting", severity="low", problem="ORDER BY may require a sort.", why_it_matters="Sorting a large intermediate result consumes memory and CPU.", recommended_change="Keep the order only when required; consider a compatible index after measuring.", expected_benefit="Potentially less sort work.", trade_off="An ordering index adds storage and write cost."))
    if re.search(r"\bDISTINCT\b", text):
        findings.append(Finding(category="distinct", severity="medium", problem="DISTINCT removes duplicate rows after the query logic.", why_it_matters="It may introduce a sort or hash operation.", recommended_change="Remove it when joins and grouping already guarantee uniqueness.", expected_benefit="Less memory and CPU.", trade_off="Removing it when duplicates are meaningful changes results."))
    structure = {"tables": tables, "joins": len(joins), "has_filter": bool(tree.find(exp.Where)), "has_order": bool(tree.find(exp.Order)), "has_group_by": bool(tree.find(exp.Group))}
    return Analysis(tables=tables, findings=findings, structure=structure, warnings=["Estimated benefits are theoretical until measured on representative data."])
