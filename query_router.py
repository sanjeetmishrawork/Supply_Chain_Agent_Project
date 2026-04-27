# query_router.py

import json
from llm.llm_client import call_llm


def route_user_query(user_input):
    """
    LLM-powered Query Planner

    Purpose:
    Convert natural language business questions
    into a structured query plan.

    IMPORTANT:
    This function does NOT answer.
    It only creates the plan.

    Philosophy:
    LLM decides WHAT
    System decides HOW
    """

    prompt = f"""
You are a Supply Chain Query Planner.

Your job is to convert user business questions
into a structured query plan.

DO NOT answer the question.
DO NOT explain.
DO NOT provide recommendations.

Return ONLY valid JSON.

The query plan should be flexible and open-ended.

Required fields:
- intent
- entity_type

Optional fields:
- entity_value
- metric
- aggregation
- limit
- filters
- time_horizon
- comparison_target
- reasoning_hint

Intent options include:
- product_diagnosis
- category_analysis
- store_analysis
- recommendation_request
- business_impact
- forecasting_query
- ranking_query
- comparison_query
- trend_query

Entity types include:
- item_id
- category
- store_id
- none

Examples:

User:
Why is FOODS risky?

Return:
{{
    "intent": "category_analysis",
    "entity_type": "category",
    "entity_value": "FOODS",
    "metric": "inventory_risk",
    "reasoning_hint": "diagnose operational issue"
}}

User:
What are the top 3 stores
with highest stockout risk?

Return:
{{
    "intent": "ranking_query",
    "entity_type": "store_id",
    "metric": "stockout_risk",
    "aggregation": "top",
    "limit": 3,
    "time_horizon": "30_days",
    "reasoning_hint": "rank operational risk"
}}

User:
Compare FOODS vs HOBBIES

Return:
{{
    "intent": "comparison_query",
    "entity_type": "category",
    "entity_value": "FOODS",
    "comparison_target": "HOBBIES",
    "metric": "inventory_risk",
    "reasoning_hint": "compare business risk"
}}

User:
Will FOODS_3_711 stock out next week?

Return:
{{
    "intent": "forecasting_query",
    "entity_type": "item_id",
    "entity_value": "FOODS_3_711",
    "metric": "stockout_risk",
    "time_horizon": "7_days",
    "reasoning_hint": "future stockout prediction"
}}

Now process this user question:

User:
{user_input}

Return ONLY JSON.
"""

    print("\n--- Calling LLM for Query Planning ---\n")

    response = call_llm(prompt)

    print("Raw Router Response:")
    print(response)

    # -----------------------------------
    # Safe JSON Parsing
    # -----------------------------------

    try:
        parsed_response = json.loads(
            response.strip()
        )

        print("\nStructured Query Plan:")
        print(parsed_response)

        return parsed_response

    except Exception as e:
        print(
            "\nRouter parsing failed:",
            str(e)
        )

        # Safe fallback
        return {
            "intent": "executive_summary",
            "entity_type": "none",
            "reasoning_hint": "fallback route"
        }