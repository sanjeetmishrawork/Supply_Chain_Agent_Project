
# query_dsl_builder.py

def build_query_dsl(query_plan):
    """
    Query DSL Builder

    Purpose:
    Convert planner output into
    safe executable analytical instructions.

    This is NOT execution.

    LLM plans.
    Python executes.
    """

    intent = query_plan.get(
        "intent",
        ""
    )

    entity_type = query_plan.get(
        "entity_type",
        ""
    )

    entity_value = query_plan.get(
        "entity_value",
        ""
    )

    metric = query_plan.get(
        "metric",
        ""
    )

    aggregation = query_plan.get(
        "aggregation",
        ""
    )

    limit = query_plan.get(
        "limit",
        5
    )

    comparison_target = query_plan.get(
        "comparison_target",
        ""
    )

    operation = query_plan.get(
        "operation",
        ""
    )

    target_field = query_plan.get(
        "target_field",
        ""
    )

    threshold = query_plan.get(
        "threshold",
        None
    )

    # =====================================
    # SAFETY CHECK
    # =====================================

    if intent in [
        "product_diagnosis",
        "category_analysis",
        "department_analysis",
        "store_analysis",
        "state_analysis",
        "comparison_query",
        "root_cause_query"
    ]:
        if (
            entity_type != "none"
            and not entity_value
        ):
            raise ValueError(
                f"Missing entity_value for "
                f"intent={intent}, "
                f"entity_type={entity_type}"
            )

    # =====================================
    # BASE DSL
    # =====================================

    dsl = {
        "source": "gold_inventory_risk",
        "query_type": "generic_analysis",
        "filters": [],
        "group_by": [],
        "aggregations": [],
        "sort": {
            "field": None,
            "order": "desc"
        },
        "limit": limit,
        "comparison": None,
        "time_window": None,
        "metric": metric,
        "operation": None,
        "target_field": None,
        "threshold": threshold
    }

    # =====================================
    # SOURCE ROUTING
    # =====================================

    if metric == "anomaly_score":
        dsl["source"] = "gold_demand_anomaly"

    elif metric == "stockout_risk":
        dsl["source"] = "gold_stockout_risk"

    elif metric in [
        "forecast_next_7_days",
        "forecast_next_30_days"
    ]:
        dsl["source"] = "gold_demand_forecast"

    elif metric == "price_sensitivity":
        dsl["source"] = "gold_price_impact"

    else:
        dsl["source"] = "gold_inventory_risk"

    # =====================================
    # ENTITY FILTERS
    # =====================================

    if entity_type == "category" and entity_value:
        dsl["filters"].append({
            "field": "category",
            "operator": "=",
            "value": entity_value.upper()
        })

    elif entity_type == "department" and entity_value:
        dsl["filters"].append({
            "field": "department",
            "operator": "=",
            "value": entity_value.upper()
        })

    elif entity_type == "item_id" and entity_value:
        dsl["filters"].append({
            "field": "item_id",
            "operator": "=",
            "value": entity_value.upper()
        })

    elif entity_type == "store_id" and entity_value:
        dsl["filters"].append({
            "field": "store_id",
            "operator": "=",
            "value": entity_value.upper()
        })

    elif entity_type == "state_id" and entity_value:
        dsl["filters"].append({
            "field": "state_id",
            "operator": "=",
            "value": entity_value.upper()
        })

    # =====================================
    # DISCOVERY QUERY
    # =====================================

    if intent == "discovery_query":

        dsl["query_type"] = "discovery"

        dsl["operation"] = (
            operation
            or "distinct_values"
        )

        dsl["target_field"] = (
            target_field
            or "category"
        )

        dsl["metric"] = None
        dsl["aggregations"] = []
        dsl["comparison"] = None
        dsl["limit"] = None

        return dsl

    # =====================================
    # RANKING QUERY
    # =====================================

    elif intent == "ranking_query":

        dsl["query_type"] = "ranking"

        if entity_type == "category":
            dsl["group_by"] = ["category"]

        elif entity_type == "store_id":
            dsl["group_by"] = ["store_id"]

        elif entity_type == "item_id":
            dsl["group_by"] = ["item_id"]

        elif entity_type == "department":
            dsl["group_by"] = ["department"]

        elif entity_type == "state_id":
            dsl["group_by"] = ["state_id"]

        dsl["aggregations"] = [
            {
                "function": "sum",
                "field": metric,
                "alias": "score"
            }
        ]

        dsl["sort"] = {
            "field": "score",
            "order": (
                "desc"
                if aggregation == "top"
                else "asc"
            )
        }

        dsl["limit"] = limit or 5

    # =====================================
    # COMPARISON QUERY
    # =====================================

    elif intent == "comparison_query":

        dsl["query_type"] = "comparison"

        if not comparison_target:
            raise ValueError(
                "comparison_target missing "
                "for comparison_query"
            )

        dsl["comparison"] = {
            "left": entity_value.upper(),
            "right": comparison_target.upper(),
            "metric": metric
        }

    # =====================================
    # FORECAST QUERY
    # =====================================

    elif intent == "forecasting_query":

        dsl["query_type"] = "forecast"

        dsl["source"] = (
            "gold_demand_forecast"
        )

        dsl["aggregations"] = [
            {
                "function": "mean",
                "field": "forecast_next_30_days",
                "alias": "forecast_value"
            }
        ]

    # =====================================
    # THRESHOLD QUERY
    # =====================================

    elif intent == "threshold_query":

        dsl["query_type"] = "threshold"

        dsl["aggregations"] = []

        dsl["sort"] = {
            "field": metric,
            "order": "desc"
        }

        dsl["limit"] = limit or 20

    # =====================================
    # ROOT CAUSE / DIAGNOSTIC
    # =====================================

    elif intent in [
        "product_diagnosis",
        "category_analysis",
        "department_analysis",
        "store_analysis",
        "state_analysis",
        "root_cause_query",
        "recommendation_request",
        "business_impact",
        "portfolio_summary",
        "intervention_priority",
        "price_sensitivity_query",
        "exception_query"
    ]:

        dsl["query_type"] = (
            "diagnostic_analysis"
        )

        dsl["aggregations"] = [
            {
                "function": "summary",
                "field": metric,
                "alias": "diagnostic_summary"
            }
        ]

    # =====================================
    # FALLBACK
    # =====================================

    else:
        dsl["query_type"] = "fallback"

    return dsl

