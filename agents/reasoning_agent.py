
# agents/reasoning_agent.py

from llm.summary_llm import get_summary_from_llm


def build_reasoning_context(
    query_plan,
    query_context
):
    """
    Build structured reasoning payload

    Purpose:
    Convert execution output into
    executive reasoning context.

    IMPORTANT:
    Query-type aware.
    No generic polished nonsense.
    """

    context_lines = []

    intent = query_plan.get(
        "intent",
        "unknown"
    )

    query_type = query_context.get(
        "query_type",
        "unknown"
    )

    context_lines.append(
        f"Intent: {intent}"
    )

    context_lines.append(
        f"Query Type: {query_type}"
    )

    # =====================================
    # RANKING
    # =====================================

    if query_type == "ranking":

        context_lines.append(
            f"Metric: "
            f"{query_context.get('metric', 'N/A')}"
        )

        ranking_results = query_context.get(
            "ranking_results",
            []
        )

        context_lines.append(
            "Ranking Results:"
        )

        if ranking_results:
            for idx, row in enumerate(
                ranking_results,
                start=1
            ):
                entity_name = None
                score = row.get(
                    "score",
                    "N/A"
                )

                for field in [
                    "item_id",
                    "category",
                    "store_id",
                    "department",
                    "state_id"
                ]:
                    if field in row:
                        entity_name = (
                            f"{field} = "
                            f"{row[field]}"
                        )
                        break

                if not entity_name:
                    entity_name = str(row)

                context_lines.append(
                    f"{idx}. "
                    f"{entity_name} "
                    f"| score = {score}"
                )
        else:
            context_lines.append(
                "No ranking results found"
            )

    # =====================================
    # COMPARISON
    # =====================================

    elif query_type == "comparison":

        context_lines.append(
            f"Comparison Metric: "
            f"{query_context.get('metric', 'N/A')}"
        )

        left_entity = query_context.get(
            "left_entity",
            {}
        )

        right_entity = query_context.get(
            "right_entity",
            {}
        )

        context_lines.append(
            "Left Entity:"
        )
        context_lines.append(
            str(left_entity)
        )

        context_lines.append(
            "Right Entity:"
        )
        context_lines.append(
            str(right_entity)
        )

    # =====================================
    # FORECAST
    # =====================================

    elif query_type == "forecast":

        if "forecast_next_30_days" in query_context:
            context_lines.append(
                f"Forecast Next 30 Days: "
                f"{query_context['forecast_next_30_days']}"
            )

        context_lines.append(
            f"Forecast Metric: "
            f"{query_context.get('metric', 'N/A')}"
        )

    # =====================================
    # PRODUCT ANALYSIS
    # =====================================

    elif query_type == "product_analysis":

        fields = [
            "item_id",
            "total_stores",
            "avg_daily_sales",
            "high_risk_store_count",
            "highest_risk_store",
            "dominant_risk_level"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # CATEGORY ANALYSIS
    # =====================================

    elif query_type == "category_analysis":

        fields = [
            "category",
            "total_items",
            "avg_daily_sales",
            "high_risk_count",
            "top_store"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # STORE ANALYSIS
    # =====================================

    elif query_type == "store_analysis":

        fields = [
            "store_id",
            "total_products",
            "avg_daily_sales",
            "high_risk_products",
            "top_category"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # DEPARTMENT ANALYSIS
    # =====================================

    elif query_type == "department_analysis":

        fields = [
            "department",
            "total_items",
            "avg_daily_sales",
            "high_risk_count"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # STATE ANALYSIS
    # =====================================

    elif query_type == "state_analysis":

        fields = [
            "state_id",
            "total_items",
            "avg_daily_sales",
            "high_risk_count",
            "top_category"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # ROOT CAUSE
    # =====================================

    elif intent == "root_cause_query":

        context_lines.append(
            "Root Cause Analysis:"
        )

        fields = [
            "category",
            "item_id",
            "store_id",
            "high_risk_count",
            "avg_daily_sales",
            "zero_sales_days",
            "sales_volatility",
            "dominant_risk_level"
        ]

        for field in fields:
            if field in query_context:
                context_lines.append(
                    f"{field}: "
                    f"{query_context[field]}"
                )

    # =====================================
    # THRESHOLD QUERY
    # =====================================

    elif query_type == "threshold":

        context_lines.append(
            f"Threshold Metric: "
            f"{query_context.get('metric', 'N/A')}"
        )

        if "threshold" in query_context:
            context_lines.append(
                f"Threshold Value: "
                f"{query_context['threshold']}"
            )

        if "ranking_results" in query_context:
            context_lines.append(
                str(query_context["ranking_results"])
            )

    # =====================================
    # PRICE SENSITIVITY
    # =====================================

    elif intent == "price_sensitivity_query":

        context_lines.append(
            "Price Sensitivity Analysis:"
        )

        for key, value in query_context.items():
            if key not in [
                "query_type"
            ]:
                context_lines.append(
                    f"{key}: {value}"
                )

    # =====================================
    # PORTFOLIO SUMMARY
    # =====================================

    elif intent == "portfolio_summary":

        context_lines.append(
            "Portfolio Summary:"
        )

        for key, value in query_context.items():
            if key not in [
                "query_type"
            ]:
                context_lines.append(
                    f"{key}: {value}"
                )

    # =====================================
    # INTERVENTION PRIORITY
    # =====================================

    elif intent == "intervention_priority":

        context_lines.append(
            "Intervention Priority:"
        )

        for key, value in query_context.items():
            if key not in [
                "query_type"
            ]:
                context_lines.append(
                    f"{key}: {value}"
                )

    # =====================================
    # EXCEPTION QUERY
    # =====================================

    elif intent == "exception_query":

        context_lines.append(
            "Exception Detection:"
        )

        for key, value in query_context.items():
            if key not in [
                "query_type"
            ]:
                context_lines.append(
                    f"{key}: {value}"
                )

    # =====================================
    # FALLBACK
    # =====================================

    else:

        for key, value in query_context.items():
            if key != "query_type":
                context_lines.append(
                    f"{key}: {value}"
                )

    # =====================================
    # REASONING GOAL
    # =====================================

    if "reasoning_hint" in query_plan:
        context_lines.append(
            f"Reasoning Goal: "
            f"{query_plan['reasoning_hint']}"
        )

    return "\n".join(context_lines)


def generate_business_reasoning(
    query_plan,
    query_context
):
    """
    Final Business Reasoning Agent

    Facts first.
    Then reasoning.

    Never reverse that.
    """

    print(
        "\n--- Business Reasoning Agent ---\n"
    )

    reasoning_context = build_reasoning_context(
        query_plan,
        query_context
    )

    print(
        "Reasoning Context:\n"
    )
    print(reasoning_context)

    print(
        "\n--- Calling Final Summary LLM ---\n"
    )

    final_response = get_summary_from_llm(
        reasoning_context
    )

    print(
        "\nFinal Executive Response:\n"
    )
    print(final_response)

    print(
        "\n-----------------------------------\n"
    )

    return final_response
