# # agents/reasoning_agent.py

# from llm.summary_llm import get_summary_from_llm


# def build_reasoning_context(
#     query_plan,
#     query_context
# ):
#     """
#     Build structured reasoning payload

#     Purpose:
#     Convert execution output into
#     executive reasoning context.

#     IMPORTANT:
#     This must be intent-aware.

#     ranking_query != comparison_query

#     Same template for all queries
#     creates polished nonsense.

#     We avoid that.
#     """

#     context_lines = []

#     intent = query_plan.get(
#         "intent",
#         "unknown"
#     )

#     query_type = query_context.get(
#         "query_type",
#         "unknown"
#     )

#     context_lines.append(
#         f"Intent: {intent}"
#     )

#     context_lines.append(
#         f"Query Type: {query_type}"
#     )

#     # =====================================
#     # RANKING QUERY
#     # =====================================

#     if query_type == "ranking":

#         context_lines.append(
#             f"Metric: {query_context.get('metric', 'N/A')}"
#         )

#         ranking_results = query_context.get(
#             "ranking_results",
#             []
#         )

#         context_lines.append(
#             "Ranking Results:"
#         )

#         if ranking_results:
#             for idx, row in enumerate(
#                 ranking_results,
#                 start=1
#             ):
#                 row_text = (
#                     f"{idx}. {row}"
#                 )
#                 context_lines.append(
#                     row_text
#                 )
#         else:
#             context_lines.append(
#                 "No ranking results found"
#             )

#     # =====================================
#     # COMPARISON QUERY
#     # =====================================

#     elif query_type == "comparison":

#         context_lines.append(
#             f"Comparison Metric: {query_context.get('metric', 'N/A')}"
#         )

#         left_entity = query_context.get(
#             "left_entity",
#             {}
#         )

#         right_entity = query_context.get(
#             "right_entity",
#             {}
#         )

#         context_lines.append(
#             "Left Entity:"
#         )
#         context_lines.append(
#             str(left_entity)
#         )

#         context_lines.append(
#             "Right Entity:"
#         )
#         context_lines.append(
#             str(right_entity)
#         )

#     # =====================================
#     # FORECAST QUERY
#     # =====================================

#     elif query_type == "forecast":

#         if "forecast_next_30_days" in query_context:
#             context_lines.append(
#                 f"Forecast Next 30 Days: "
#                 f"{query_context['forecast_next_30_days']}"
#             )

#         context_lines.append(
#             f"Forecast Metric: {query_context.get('metric', 'N/A')}"
#         )

#     # =====================================
#     # CATEGORY / PRODUCT / STORE ANALYSIS
#     # =====================================

#     else:

#         if "item_id" in query_context:
#             context_lines.append(
#                 f"Item: {query_context['item_id']}"
#             )

#         if "category" in query_context:
#             context_lines.append(
#                 f"Category: {query_context['category']}"
#             )

#         if "store_id" in query_context:
#             context_lines.append(
#                 f"Store: {query_context['store_id']}"
#             )

#         if "inventory_risk" in query_context:
#             context_lines.append(
#                 f"Inventory Risk: "
#                 f"{query_context['inventory_risk']}"
#             )

#         if "forecast_next_30_days" in query_context:
#             context_lines.append(
#                 f"30-Day Forecast Demand: "
#                 f"{query_context['forecast_next_30_days']}"
#             )

#         if "stockout_risk" in query_context:
#             context_lines.append(
#                 f"Stockout Risk: "
#                 f"{query_context['stockout_risk']}"
#             )

#         if "days_to_stockout" in query_context:
#             context_lines.append(
#                 f"Days to Stockout: "
#                 f"{query_context['days_to_stockout']}"
#             )

#         if "high_stockout_items" in query_context:
#             context_lines.append(
#                 f"High Stockout Items: "
#                 f"{query_context['high_stockout_items']}"
#             )

#         if "high_risk_count" in query_context:
#             context_lines.append(
#                 f"High Risk Count: "
#                 f"{query_context['high_risk_count']}"
#             )

#         if "top_store" in query_context:
#             context_lines.append(
#                 f"Top Store: "
#                 f"{query_context['top_store']}"
#             )

#     # =====================================
#     # REASONING GOAL
#     # =====================================

#     if "reasoning_hint" in query_plan:
#         context_lines.append(
#             f"Reasoning Goal: "
#             f"{query_plan['reasoning_hint']}"
#         )

#     return "\n".join(context_lines)


# def generate_business_reasoning(
#     query_plan,
#     query_context
# ):
#     """
#     Final Business Reasoning Agent

#     Purpose:
#     Create executive-grade explanation
#     using real execution output.

#     This is:
#     final strategic interpretation.

#     Facts first.
#     Then reasoning.

#     Never reverse that.
#     """

#     print(
#         "\n--- Business Reasoning Agent ---\n"
#     )

#     reasoning_context = build_reasoning_context(
#         query_plan,
#         query_context
#     )

#     print(
#         "Reasoning Context:\n"
#     )
#     print(reasoning_context)

#     print(
#         "\n--- Calling Final Summary LLM ---\n"
#     )

#     final_response = get_summary_from_llm(
#         reasoning_context
#     )

#     print(
#         "\nFinal Executive Response:\n"
#     )
#     print(final_response)

#     print(
#         "\n-----------------------------------\n"
#     )

#     return final_response

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
    This must be intent-aware.

    ranking_query != comparison_query

    Same template for all queries
    creates polished nonsense.

    We avoid that.
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
    # RANKING QUERY
    # =====================================

    if query_type == "ranking":

        context_lines.append(
            f"Metric: {query_context.get('metric', 'N/A')}"
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
                context_lines.append(
                    f"{idx}. {row}"
                )
        else:
            context_lines.append(
                "No ranking results found"
            )

    # =====================================
    # COMPARISON QUERY
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
    # FORECAST QUERY
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
    # PRODUCT / CATEGORY / STORE ANALYSIS
    # =====================================

    else:

        # -----------------------------------
        # PRODUCT ANALYSIS
        # -----------------------------------

        if query_type == "product_analysis":

            if "item_id" in query_context:
                context_lines.append(
                    f"Item: "
                    f"{query_context['item_id']}"
                )

            if "total_stores" in query_context:
                context_lines.append(
                    f"Total Stores: "
                    f"{query_context['total_stores']}"
                )

            if "avg_daily_sales" in query_context:
                context_lines.append(
                    f"Average Daily Sales: "
                    f"{query_context['avg_daily_sales']}"
                )

            if "high_risk_store_count" in query_context:
                context_lines.append(
                    f"High Risk Store Count: "
                    f"{query_context['high_risk_store_count']}"
                )

            if "highest_risk_store" in query_context:
                context_lines.append(
                    f"Highest Risk Store: "
                    f"{query_context['highest_risk_store']}"
                )

            if "dominant_risk_level" in query_context:
                context_lines.append(
                    f"Dominant Risk Level: "
                    f"{query_context['dominant_risk_level']}"
                )

        # -----------------------------------
        # CATEGORY / STORE / GENERIC ANALYSIS
        # -----------------------------------

        else:

            if "item_id" in query_context:
                context_lines.append(
                    f"Item: "
                    f"{query_context['item_id']}"
                )

            if "category" in query_context:
                context_lines.append(
                    f"Category: "
                    f"{query_context['category']}"
                )

            if "store_id" in query_context:
                context_lines.append(
                    f"Store: "
                    f"{query_context['store_id']}"
                )

            if "inventory_risk" in query_context:
                context_lines.append(
                    f"Inventory Risk: "
                    f"{query_context['inventory_risk']}"
                )

            if "forecast_next_30_days" in query_context:
                context_lines.append(
                    f"30-Day Forecast Demand: "
                    f"{query_context['forecast_next_30_days']}"
                )

            if "stockout_risk" in query_context:
                context_lines.append(
                    f"Stockout Risk: "
                    f"{query_context['stockout_risk']}"
                )

            if "days_to_stockout" in query_context:
                context_lines.append(
                    f"Days to Stockout: "
                    f"{query_context['days_to_stockout']}"
                )

            if "high_stockout_items" in query_context:
                context_lines.append(
                    f"High Stockout Items: "
                    f"{query_context['high_stockout_items']}"
                )

            if "high_risk_count" in query_context:
                context_lines.append(
                    f"High Risk Count: "
                    f"{query_context['high_risk_count']}"
                )

            if "top_store" in query_context:
                context_lines.append(
                    f"Top Store: "
                    f"{query_context['top_store']}"
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

    Purpose:
    Create executive-grade explanation
    using real execution output.

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