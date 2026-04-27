# # query_dsl_builder.py

# def build_query_dsl(query_plan):
#     """
#     Query DSL Builder

#     Purpose:
#     Convert planner output into
#     safe executable analytical instructions.

#     IMPORTANT:

#     This is NOT execution.

#     This is:
#     controlled analytical planning.

#     No pandas here.
#     No SQL here.
#     No LLM here.

#     Only:
#     structured execution instructions.

#     We are moving from:

#     query_type-driven

#     to

#     operation-driven DSL.

#     This supports:
#     any valid analysis
#     across any gold data field.

#     Example:

#     {
#         "source": "gold_inventory_risk",

#         "filters": [
#             {
#                 "field": "risk_level",
#                 "operator": "=",
#                 "value": "HIGH"
#             }
#         ],

#         "group_by": [
#             "store_id"
#         ],

#         "aggregations": [
#             {
#                 "function": "count",
#                 "field": "item_id",
#                 "alias": "high_risk_items"
#             }
#         ],

#         "sort": {
#             "field": "high_risk_items",
#             "order": "desc"
#         },

#         "limit": 5
#     }
#     """

#     intent = query_plan.get(
#         "intent",
#         ""
#     )

#     entity_type = query_plan.get(
#         "entity_type",
#         ""
#     )

#     entity_value = query_plan.get(
#         "entity_value",
#         ""
#     )

#     metric = query_plan.get(
#         "metric",
#         ""
#     )

#     aggregation = query_plan.get(
#         "aggregation",
#         ""
#     )

#     limit = query_plan.get(
#         "limit",
#         5
#     )

#     comparison_target = query_plan.get(
#         "comparison_target",
#         ""
#     )

#     # =====================================
#     # BASE DSL
#     # =====================================

#     dsl = {
#         "source": "gold_inventory_risk",
#         "query_type": "generic_analysis",

#         "filters": [],

#         "group_by": [],

#         "aggregations": [],

#         "sort": {
#             "field": None,
#             "order": "desc"
#         },

#         "limit": limit,

#         "comparison": None,

#         "time_window": None,

#         "metric": metric
#     }

#     # =====================================
#     # ENTITY FILTER NORMALIZATION
#     # =====================================

#     if entity_type == "category" and entity_value:
#         dsl["filters"].append({
#             "field": "category",
#             "operator": "=",
#             "value": entity_value.upper()
#         })

#     elif entity_type == "item_id" and entity_value:
#         dsl["filters"].append({
#             "field": "item_id",
#             "operator": "startswith",
#             "value": entity_value.upper()
#         })

#     elif entity_type == "store_id" and entity_value:
#         dsl["filters"].append({
#             "field": "store_id",
#             "operator": "=",
#             "value": entity_value.upper()
#         })

#     # =====================================
#     # RANKING QUERY
#     # =====================================

#     if intent == "ranking_query":

#         dsl["query_type"] = "ranking"

#         # group target

#         if entity_type == "category":
#             dsl["group_by"] = [
#                 "category"
#             ]

#         elif entity_type == "store_id":
#             dsl["group_by"] = [
#                 "store_id"
#             ]

#         elif entity_type == "item_id":
#             dsl["group_by"] = [
#                 "item_id"
#             ]

#         # aggregation

#         dsl["aggregations"] = [
#             {
#                 "function": "sum",
#                 "field": metric,
#                 "alias": "score"
#             }
#         ]

#         # sorting

#         dsl["sort"] = {
#             "field": "score",
#             "order": (
#                 "desc"
#                 if aggregation == "top"
#                 else "asc"
#             )
#         }

#         dsl["limit"] = limit or 5

#     # =====================================
#     # COMPARISON QUERY
#     # =====================================

#     elif intent == "comparison_query":

#         dsl["query_type"] = "comparison"

#         dsl["comparison"] = {
#             "left": entity_value.upper(),
#             "right": comparison_target.upper(),
#             "metric": metric
#         }

#     # =====================================
#     # FORECAST QUERY
#     # =====================================

#     elif intent == "forecasting_query":

#         dsl["query_type"] = "forecast"

#         dsl["source"] = (
#             "gold_demand_forecast"
#         )

#         dsl["aggregations"] = [
#             {
#                 "function": "mean",
#                 "field": (
#                     "forecast_next_30_days"
#                 ),
#                 "alias": (
#                     "forecast_value"
#                 )
#             }
#         ]

#     # =====================================
#     # PRODUCT / CATEGORY / STORE ANALYSIS
#     # =====================================

#     elif intent in [
#         "product_diagnosis",
#         "category_analysis",
#         "store_analysis",
#         "recommendation_request",
#         "business_impact"
#     ]:

#         dsl["query_type"] = (
#             "diagnostic_analysis"
#         )

#         dsl["aggregations"] = [
#             {
#                 "function": "summary",
#                 "field": metric,
#                 "alias": "diagnostic_summary"
#             }
#         ]

#     # =====================================
#     # FALLBACK
#     # =====================================

#     else:

#         dsl["query_type"] = (
#             "fallback"
#         )

#     return dsl
# query_dsl_builder.py

def build_query_dsl(query_plan):
    """
    Query DSL Builder

    Purpose:
    Convert planner output into
    safe executable analytical instructions.

    This is NOT execution.

    This is:
    controlled analytical planning.

    Only:
    structured execution instructions.

    No pandas.
    No SQL.
    No unsafe execution.

    LLM plans.
    Python executes.

    Adult supervision.
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

        "target_field": None
    }

    # =====================================
    # ENTITY FILTER NORMALIZATION
    # =====================================

    if entity_type == "category" and entity_value:
        dsl["filters"].append({
            "field": "category",
            "operator": "=",
            "value": entity_value.upper()
        })

    elif entity_type == "item_id" and entity_value:
        dsl["filters"].append({
            "field": "item_id",
            "operator": "startswith",
            "value": entity_value.upper()
        })

    elif entity_type == "store_id" and entity_value:
        dsl["filters"].append({
            "field": "store_id",
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

        # discovery queries do not need:
        # metric
        # aggregations
        # comparison
        # ranking logic

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
            dsl["group_by"] = [
                "category"
            ]

        elif entity_type == "store_id":
            dsl["group_by"] = [
                "store_id"
            ]

        elif entity_type == "item_id":
            dsl["group_by"] = [
                "item_id"
            ]

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
                "field": (
                    "forecast_next_30_days"
                ),
                "alias": (
                    "forecast_value"
                )
            }
        ]

    # =====================================
    # PRODUCT / CATEGORY / STORE ANALYSIS
    # =====================================

    elif intent in [
        "product_diagnosis",
        "category_analysis",
        "store_analysis",
        "recommendation_request",
        "business_impact"
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

        dsl["query_type"] = (
            "fallback"
        )

    return dsl