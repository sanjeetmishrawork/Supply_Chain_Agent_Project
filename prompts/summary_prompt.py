
# prompts/summary_prompt.py

def get_summary_prompt(execution_result):
    """
    Executive Summary Prompt

    Purpose:
    Convert structured execution output
    into clear boardroom-ready business summaries.

    IMPORTANT:
    This is explanation.
    Not analysis generation.

    The executor already decided facts.

    This prompt must:
    explain clearly,
    stay concise,
    and avoid hallucination.

    No invention.
    No guessing.
    No fake strategy theatre.
    """

    query_type = execution_result.get(
        "query_type",
        "fallback"
    )

    # =====================================
    # PRODUCT ANALYSIS
    # =====================================

    if query_type == "product_analysis":

        return f"""
You are writing for senior executives.

Summarize this product-level operational case.

Product Information:
Item ID: {execution_result.get("item_id", "")}

Business Context:
Total Stores: {execution_result.get("total_stores", "")}
Average Daily Sales: {execution_result.get("avg_daily_sales", "")}
Dominant Risk Level: {execution_result.get("dominant_risk_level", "")}
High Risk Store Count: {execution_result.get("high_risk_store_count", "")}

Return a concise executive summary
in 4–5 lines.

It should be:
Clear
Decisive
Boardroom-ready
Strategic

Avoid technical noise.
Avoid inventing missing facts.
"""

    # =====================================
    # CATEGORY ANALYSIS
    # =====================================

    elif query_type == "category_analysis":

        return f"""
You are writing for senior executives.

Summarize this category-level operational case.

Category:
{execution_result.get("category", "")}

Business Context:
Total Items: {execution_result.get("total_items", "")}
Average Daily Sales: {execution_result.get("avg_daily_sales", "")}
High Risk Count: {execution_result.get("high_risk_count", "")}
Top Store: {execution_result.get("top_store", "")}

Return a concise executive summary
in 4–5 lines.

Focus on operational risk,
business exposure,
and immediate management attention required.

Avoid technical noise.
Avoid inventing missing facts.
"""

    # =====================================
    # STORE ANALYSIS
    # =====================================

    elif query_type == "store_analysis":

        return f"""
You are writing for senior executives.

Summarize this store-level operational case.

Store:
{execution_result.get("store_id", "")}

Business Context:
Total Products: {execution_result.get("total_products", "")}
Average Daily Sales: {execution_result.get("avg_daily_sales", "")}
High Risk Products: {execution_result.get("high_risk_products", "")}
Top Category: {execution_result.get("top_category", "")}

Return a concise executive summary
in 4–5 lines.

Focus on operational pressure,
inventory exposure,
and leadership action required.

Avoid technical noise.
Avoid inventing missing facts.
"""

    # =====================================
    # DEPARTMENT ANALYSIS
    # =====================================

    elif query_type == "department_analysis":

        return f"""
You are writing for senior executives.

Summarize this department-level operational case.

Department:
{execution_result.get("department", "")}

Business Context:
Total Items: {execution_result.get("total_items", "")}
Average Daily Sales: {execution_result.get("avg_daily_sales", "")}
High Risk Count: {execution_result.get("high_risk_count", "")}

Return a concise executive summary
in 4–5 lines.

Focus on operational concentration,
portfolio risk,
and strategic intervention.

Avoid technical noise.
Avoid inventing missing facts.
"""

    # =====================================
    # RANKING QUERY
    # =====================================

    elif query_type == "ranking":

        return f"""
You are writing for senior executives.

Summarize this ranking analysis.

Metric:
{execution_result.get("metric", "")}

Ranking Results:
{execution_result.get("ranking_results", [])}

Return a concise executive summary
in 4–5 lines.

Focus on:
top performers,
highest risk concentration,
and business implications.

Avoid technical noise.
Avoid repeating raw tables.
Interpret strategically.
"""

    # =====================================
    # COMPARISON QUERY
    # =====================================

    elif query_type == "comparison":

        return f"""
You are writing for senior executives.

Summarize this business comparison.

Metric:
{execution_result.get("metric", "")}

Left Entity:
{execution_result.get("left_entity", {})}

Right Entity:
{execution_result.get("right_entity", {})}

Return a concise executive summary
in 4–5 lines.

Focus on:
which side performs better,
where risk is concentrated,
and management implications.

Avoid technical noise.
Avoid repeating raw dictionaries.
Interpret strategically.
"""

    # =====================================
    # DISCOVERY QUERY
    # =====================================

    elif query_type == "discovery":

        return f"""
You are writing for senior executives.

Summarize this metadata discovery result.

Target Field:
{execution_result.get("target_field", "")}

Available Values:
{execution_result.get("values", [])}

Return a concise executive summary
in 3–4 lines.

Focus on:
business coverage,
available operating dimensions,
and what is available for analysis.

Avoid technical noise.
Avoid reading the list like a robot.
"""

    # =====================================
    # FORECAST QUERY
    # =====================================

    elif query_type == "forecast":

        return f"""
You are writing for senior executives.

Summarize this demand forecast result.

Forecast Next 30 Days:
{execution_result.get("forecast_next_30_days", "")}

Return a concise executive summary
in 4–5 lines.

Focus on:
future demand expectations,
inventory planning implications,
and business readiness.

Avoid technical noise.
Avoid inventing missing facts.
"""

    # =====================================
    # FALLBACK
    # =====================================

    return f"""
You are writing for senior executives.

Summarize the following result clearly:

{execution_result}

Return a concise business summary
in 4–5 lines.

Be clear.
Be direct.
Do not invent facts.
"""
