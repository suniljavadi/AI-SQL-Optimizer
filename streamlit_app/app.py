import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="AI SQL Optimizer", page_icon="SQL", layout="wide")
st.title("AI SQL Query Optimizer")
st.caption("Synthetic PostgreSQL lab | mock LLM mode | read-only analysis")
default = """SELECT *
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE YEAR(o.order_date) = 2026
ORDER BY o.order_date DESC;"""
sql = st.text_area("SQL query", value=default, height=180)
if st.button("Analyze and optimize", type="primary"):
    try:
        response = requests.post(f"{API_URL}/api/v1/optimize", json={"sql": sql}, timeout=10)
        response.raise_for_status()
        result = response.json()
        left, right = st.columns(2)
        with left:
            st.subheader("Findings")
            for finding in result["analysis"]["findings"]:
                with st.expander(f"{finding['severity'].upper()} · {finding['problem']}"):
                    st.write(f"**Why:** {finding['why_it_matters']}")
                    st.write(f"**Change:** {finding['recommended_change']}")
                    st.write(f"**Benefit:** {finding['expected_benefit']}")
                    st.write(f"**Trade-off:** {finding['trade_off']}")
        with right:
            st.subheader("Optimized SQL")
            st.code(result["optimized_sql"], language="sql")
            st.subheader("Index recommendations")
            for index in result["indexes"]:
                st.code(index, language="sql")
            st.info(result["estimated_improvement"])
        st.subheader("Comparison")
        comparison = requests.post(f"{API_URL}/api/v1/compare", json={"original_sql": sql, "optimized_sql": result["optimized_sql"]}, timeout=10).json()
        st.warning(comparison["message"])
        if st.button("Run optimized query on synthetic database"):
            execution = requests.post(f"{API_URL}/api/v1/execute", json={"sql": result["optimized_sql"]}, timeout=10).json()
            if execution.get("executed"):
                st.write({"execution_ms": execution["execution_ms"], "rows_returned": execution["row_count"], "theoretical": execution["theoretical"]})
                st.dataframe(execution["rows"])
            else:
                st.error("Synthetic execution unavailable: " + "; ".join(execution.get("errors", [])))
    except requests.RequestException as error:
        st.error(f"API unavailable: {error}")
