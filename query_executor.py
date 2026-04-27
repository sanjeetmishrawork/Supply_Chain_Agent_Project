# # # query_executor.py

# # import pandas as pd
# # import glob


# # def load_demand_forecast():
# #     """
# #     Load demand forecast
# #     from multiple CSV files
# #     """

# #     files = glob.glob(
# #         "data/gold_demand_forecast/*.csv"
# #     )

# #     if not files:
# #         return pd.DataFrame()

# #     return pd.concat(
# #         [pd.read_csv(f) for f in files],
# #         ignore_index=True
# #     )


# # def load_stockout_risk():
# #     """
# #     Load stockout risk
# #     from multiple CSV files
# #     """

# #     files = glob.glob(
# #         "data/gold_stockout_risk/*.csv"
# #     )

# #     if not files:
# #         return pd.DataFrame()

# #     return pd.concat(
# #         [pd.read_csv(f) for f in files],
# #         ignore_index=True
# #     )


# # def extract_category(item_id):
# #     """
# #     Example:

# #     FOODS_001_CA_1
# #     -> FOODS
# #     """

# #     if not isinstance(item_id, str):
# #         return ""

# #     return item_id.split("_")[0].upper()


# # def apply_filters(df, filters):
# #     """
# #     Safe filter application
# #     """

# #     filtered_df = df.copy()

# #     if not filters:
# #         return filtered_df

# #     # -----------------------------------
# #     # category filter
# #     # -----------------------------------

# #     if "category" in filters:
# #         category_value = filters[
# #             "category"
# #         ].upper()

# #         filtered_df = filtered_df[
# #             filtered_df["item_id"]
# #             .str.upper()
# #             .str.startswith(category_value)
# #         ]

# #     # -----------------------------------
# #     # item_id exact filter
# #     # -----------------------------------

# #     if "item_id" in filters:
# #         item_value = filters["item_id"].upper()

# #         filtered_df = filtered_df[
# #             filtered_df["item_id"]
# #             .str.upper()
# #             .str.startswith(item_value)
# #             ]

# #     # if "item_id" in filters:
# #     #     item_value = filters[
# #     #         "item_id"
# #     #     ].upper()

# #     #     filtered_df = filtered_df[
# #     #         filtered_df["item_id"]
# #     #         .str.upper()
# #     #         == item_value
# #     #     ]

# #     # -----------------------------------
# #     # store_id exact filter
# #     # -----------------------------------

# #     if "store_id" in filters:
# #         store_value = filters[
# #             "store_id"
# #         ].upper()

# #         filtered_df = filtered_df[
# #             filtered_df["store_id"]
# #             .str.upper()
# #             == store_value
# #         ]

# #     return filtered_df


# # def map_risk_level_to_score(value):
# #     """
# #     Convert string risk labels
# #     into numeric values.

# #     Because:

# #     LOW + LOW + MEDIUM

# #     should not become:

# #     LOWLOWMEDIUM

# #     Pandas tried.
# #     We stop it.
# #     """

# #     mapping = {
# #         "LOW": 1,
# #         "MEDIUM": 2,
# #         "HIGH": 3
# #     }

# #     if pd.isna(value):
# #         return 0

# #     return mapping.get(
# #         str(value).upper(),
# #         0
# #     )


# # def execute_query_plan(
# #     inventory_df,
# #     dsl
# # ):
# #     """
# #     Safe Query Executor

# #     Executes DSL only.

# #     No raw LLM execution.
# #     No unsafe operations.
# #     """

# #     demand_df = load_demand_forecast()
# #     stockout_df = load_stockout_risk()

# #     query_type = dsl.get(
# #         "query_type",
# #         "fallback"
# #     )

# #     filters = dsl.get(
# #         "filters",
# #         {}
# #     )

# #     metric = dsl.get(
# #         "metric",
# #         ""
# #     )

# #     # -----------------------------------
# #     # Derived category column
# #     # -----------------------------------

# #     inventory_df = inventory_df.copy()

# #     inventory_df["category"] = (
# #         inventory_df["item_id"]
# #         .apply(extract_category)
# #     )

# #     # =====================================
# #     # CATEGORY ANALYSIS
# #     # =====================================

# #     if query_type == "category_analysis":

# #         matched_rows = apply_filters(
# #             inventory_df,
# #             filters
# #         )

# #         if matched_rows.empty:
# #             return {}

# #         high_risk_rows = matched_rows[
# #             matched_rows["risk_level"]
# #             == "HIGH"
# #         ]

# #         top_store = (
# #             matched_rows["store_id"]
# #             .mode()[0]
# #         )

# #         return {
# #             "query_type": "category_analysis",
# #             "category": filters.get(
# #                 "category",
# #                 ""
# #             ),
# #             "total_items": len(
# #                 matched_rows
# #             ),
# #             "high_risk_count": len(
# #                 high_risk_rows
# #             ),
# #             "top_store": top_store
# #         }

# #     # =====================================
# #     # PRODUCT ANALYSIS
# #     # =====================================

# #     elif query_type == "product_analysis":

# #         matched_rows = apply_filters(
# #             inventory_df,
# #             filters
# #         )

# #         if matched_rows.empty:
# #             return {}

# #         first_row = matched_rows.iloc[0]

# #         return {
# #             "query_type": "product_analysis",
# #             "item_id": first_row.get(
# #                 "item_id",
# #                 ""
# #             ),
# #             "store_id": first_row.get(
# #                 "store_id",
# #                 ""
# #             ),
# #             "avg_daily_sales": float(
# #                 first_row.get(
# #                     "avg_daily_sales",
# #                     0
# #                 )
# #             ),
# #             "risk_level": first_row.get(
# #                 "risk_level",
# #                 "UNKNOWN"
# #             )
# #         }

# #     # =====================================
# #     # RANKING QUERY
# #     # =====================================

# #     elif query_type == "ranking":

# #         matched_rows = apply_filters(
# #             inventory_df,
# #             filters
# #         )

# #         if matched_rows.empty:
# #             return {}

# #         group_by = dsl.get(
# #             "group_by",
# #             None
# #         )

# #         limit = dsl.get(
# #             "limit",
# #             5
# #         )

# #         sort_order = dsl.get(
# #             "sort_order",
# #             "desc"
# #         )

# #         if not group_by:
# #             return {}

# #         # -----------------------------------
# #         # Metric mapping
# #         # -----------------------------------

# #         if metric in [
# #             "sales",
# #             "avg_daily_sales"
# #         ]:
# #             value_column = (
# #                 "avg_daily_sales"
# #             )

# #         elif metric == "inventory_risk":
# #             value_column = (
# #                 "risk_score"
# #             )

# #             matched_rows[
# #                 "risk_score"
# #             ] = matched_rows[
# #                 "risk_level"
# #             ].apply(
# #                 map_risk_level_to_score
# #             )

# #         elif metric == "stockout_risk":
# #             value_column = (
# #                 "risk_score"
# #             )

# #             matched_rows[
# #                 "risk_score"
# #             ] = matched_rows[
# #                 "risk_level"
# #             ].apply(
# #                 map_risk_level_to_score
# #             )

# #         else:
# #             value_column = (
# #                 "avg_daily_sales"
# #             )

# #         # -----------------------------------
# #         # Execute grouping
# #         # -----------------------------------

# #         grouped = (
# #             matched_rows
# #             .groupby(group_by)[value_column]
# #             .sum()
# #             .reset_index(name="score")
# #         )

# #         ascending = (
# #             False
# #             if sort_order == "desc"
# #             else True
# #         )

# #         grouped = grouped.sort_values(
# #             by="score",
# #             ascending=ascending
# #         ).head(limit)

# #         return {
# #             "query_type": "ranking",
# #             "metric": metric,
# #             "ranking_results": grouped.to_dict(
# #                 orient="records"
# #             )
# #         }

# #     # =====================================
# #     # COMPARISON QUERY
# #     # =====================================

# #     elif query_type == "comparison":

# #         left_entity = filters.get(
# #             "left_entity",
# #             ""
# #         )

# #         right_entity = filters.get(
# #             "right_entity",
# #             ""
# #         )

# #         left_rows = inventory_df[
# #             inventory_df["category"]
# #             == left_entity
# #         ]

# #         right_rows = inventory_df[
# #             inventory_df["category"]
# #             == right_entity
# #         ]

# #         if (
# #             left_rows.empty
# #             or right_rows.empty
# #         ):
# #             return {}

# #         def summarize(df):
# #             high_risk_count = len(
# #                 df[
# #                     df["risk_level"]
# #                     == "HIGH"
# #                 ]
# #             )

# #             top_store = (
# #                 df["store_id"]
# #                 .mode()[0]
# #             )

# #             return {
# #                 "total_items": len(df),
# #                 "high_risk_count": high_risk_count,
# #                 "top_store": top_store
# #             }

# #         return {
# #             "query_type": "comparison",
# #             "metric": metric,
# #             "left_entity": {
# #                 "name": left_entity,
# #                 **summarize(left_rows)
# #             },
# #             "right_entity": {
# #                 "name": right_entity,
# #                 **summarize(right_rows)
# #             }
# #         }

# #     # =====================================
# #     # FORECAST QUERY
# #     # =====================================

# #     elif query_type == "forecast":

# #         matched_rows = apply_filters(
# #             demand_df,
# #             filters
# #         )

# #         if matched_rows.empty:
# #             return {}

# #         avg_forecast = round(
# #             matched_rows[
# #                 "forecast_next_30_days"
# #             ].mean(),
# #             2
# #         )

# #         return {
# #             "query_type": "forecast",
# #             "metric": metric,
# #             "forecast_next_30_days": avg_forecast
# #         }

# #     # =====================================
# #     # FALLBACK
# #     # =====================================

# #     return {
# #         "query_type": "fallback",
# #         "message": (
# #             "No matching query execution path found."
# #         )
# #     }

# # query_executor.py

# import pandas as pd
# import glob


# # =====================================
# # DATA LOADERS
# # =====================================

# def load_demand_forecast():
#     """
#     Load demand forecast
#     from multiple CSV files
#     """

#     files = glob.glob(
#         "data/gold_demand_forecast/*.csv"
#     )

#     if not files:
#         return pd.DataFrame()

#     return pd.concat(
#         [pd.read_csv(f) for f in files],
#         ignore_index=True
#     )


# def load_stockout_risk():
#     """
#     Load stockout risk
#     from multiple CSV files
#     """

#     files = glob.glob(
#         "data/gold_stockout_risk/*.csv"
#     )

#     if not files:
#         return pd.DataFrame()

#     return pd.concat(
#         [pd.read_csv(f) for f in files],
#         ignore_index=True
#     )


# # =====================================
# # SHARED HELPERS
# # =====================================

# def extract_category(item_id):
#     """
#     Example:
#     FOODS_1_005 -> FOODS
#     """

#     if not isinstance(item_id, str):
#         return ""

#     return item_id.split("_")[0].upper()


# def map_risk_level_to_score(value):
#     """
#     Convert risk labels
#     to numeric values

#     LOW -> 1
#     MEDIUM -> 2
#     HIGH -> 3
#     """

#     mapping = {
#         "LOW": 1,
#         "MEDIUM": 2,
#         "HIGH": 3
#     }

#     if pd.isna(value):
#         return 0

#     return mapping.get(
#         str(value).upper(),
#         0
#     )


# def apply_filters(df, filters):
#     """
#     Safe filter application
#     """

#     filtered_df = df.copy()

#     if not filters:
#         return filtered_df

#     # -----------------------------------
#     # category filter
#     # -----------------------------------

#     if "category" in filters:
#         category_value = filters[
#             "category"
#         ].upper()

#         filtered_df = filtered_df[
#             filtered_df["item_id"]
#             .str.upper()
#             .str.startswith(category_value)
#         ]

#     # -----------------------------------
#     # item_id prefix filter
#     # -----------------------------------

#     if "item_id" in filters:
#         item_value = filters[
#             "item_id"
#         ].upper()

#         filtered_df = filtered_df[
#             filtered_df["item_id"]
#             .str.upper()
#             .str.startswith(item_value)
#         ]

#     # -----------------------------------
#     # store_id exact filter
#     # -----------------------------------

#     if "store_id" in filters:
#         store_value = filters[
#             "store_id"
#         ].upper()

#         filtered_df = filtered_df[
#             filtered_df["store_id"]
#             .str.upper()
#             == store_value
#         ]

#     return filtered_df


# def fallback_response():
#     return {
#         "query_type": "fallback",
#         "message": (
#             "No matching query execution path found."
#         )
#     }


# # =====================================
# # EXECUTION HANDLERS
# # =====================================

# def execute_category_analysis(
#     inventory_df,
#     filters,
#     metric
# ):
#     matched_rows = apply_filters(
#         inventory_df,
#         filters
#     )

#     if matched_rows.empty:
#         return {}

#     high_risk_rows = matched_rows[
#         matched_rows["risk_level"] == "HIGH"
#     ]

#     top_store = (
#         matched_rows["store_id"]
#         .mode()[0]
#     )

#     return {
#         "query_type": "category_analysis",
#         "category": filters.get(
#             "category",
#             ""
#         ),
#         "total_items": len(
#             matched_rows
#         ),
#         "high_risk_count": len(
#             high_risk_rows
#         ),
#         "top_store": top_store
#     }


# def execute_product_analysis(
#     inventory_df,
#     filters,
#     metric
# ):
#     matched_rows = apply_filters(
#         inventory_df,
#         filters
#     )

#     if matched_rows.empty:
#         return {}

#     item_id = (
#         matched_rows["item_id"]
#         .iloc[0]
#     )

#     total_stores = (
#         matched_rows["store_id"]
#         .nunique()
#     )

#     avg_daily_sales = round(
#         matched_rows[
#             "avg_daily_sales"
#         ].mean(),
#         2
#     )

#     high_risk_rows = matched_rows[
#         matched_rows["risk_level"] == "HIGH"
#     ]

#     high_risk_store_count = (
#         high_risk_rows["store_id"]
#         .nunique()
#     )

#     dominant_risk_level = (
#         matched_rows["risk_level"]
#         .mode()[0]
#     )

#     if not high_risk_rows.empty:
#         highest_risk_store = (
#             high_risk_rows["store_id"]
#             .mode()[0]
#         )
#     else:
#         highest_risk_store = (
#             matched_rows["store_id"]
#             .mode()[0]
#         )

#     return {
#         "query_type": "product_analysis",
#         "item_id": item_id,
#         "total_stores": int(
#             total_stores
#         ),
#         "avg_daily_sales": float(
#             avg_daily_sales
#         ),
#         "high_risk_store_count": int(
#             high_risk_store_count
#         ),
#         "highest_risk_store": highest_risk_store,
#         "dominant_risk_level": dominant_risk_level
#     }


# def execute_ranking(
#     inventory_df,
#     dsl,
#     metric
# ):
#     filters = dsl.get(
#         "filters",
#         {}
#     )

#     matched_rows = apply_filters(
#         inventory_df,
#         filters
#     )

#     if matched_rows.empty:
#         return {}

#     group_by = dsl.get(
#         "group_by",
#         None
#     )

#     limit = dsl.get(
#         "limit",
#         5
#     )

#     sort_order = dsl.get(
#         "sort_order",
#         "desc"
#     )

#     if not group_by:
#         return {}

#     # -----------------------------------
#     # metric mapping
#     # -----------------------------------

#     if metric in [
#         "sales",
#         "avg_daily_sales"
#     ]:
#         value_column = (
#             "avg_daily_sales"
#         )

#     elif metric in [
#         "inventory_risk",
#         "stockout_risk"
#     ]:
#         matched_rows[
#             "risk_score"
#         ] = matched_rows[
#             "risk_level"
#         ].apply(
#             map_risk_level_to_score
#         )

#         value_column = (
#             "risk_score"
#         )

#     else:
#         value_column = (
#             "avg_daily_sales"
#         )

#     grouped = (
#         matched_rows
#         .groupby(group_by)[value_column]
#         .sum()
#         .reset_index(name="score")
#     )

#     ascending = (
#         False
#         if sort_order == "desc"
#         else True
#     )

#     grouped = grouped.sort_values(
#         by="score",
#         ascending=ascending
#     ).head(limit)

#     return {
#         "query_type": "ranking",
#         "metric": metric,
#         "ranking_results": grouped.to_dict(
#             orient="records"
#         )
#     }


# def execute_comparison(
#     inventory_df,
#     filters,
#     metric
# ):
#     left_entity = filters.get(
#         "left_entity",
#         ""
#     )

#     right_entity = filters.get(
#         "right_entity",
#         ""
#     )

#     left_rows = inventory_df[
#         inventory_df["category"]
#         == left_entity
#     ]

#     right_rows = inventory_df[
#         inventory_df["category"]
#         == right_entity
#     ]

#     if left_rows.empty or right_rows.empty:
#         return {}

#     def summarize(df):
#         high_risk_count = len(
#             df[
#                 df["risk_level"] == "HIGH"
#             ]
#         )

#         top_store = (
#             df["store_id"]
#             .mode()[0]
#         )

#         return {
#             "total_items": len(df),
#             "high_risk_count": high_risk_count,
#             "top_store": top_store
#         }

#     return {
#         "query_type": "comparison",
#         "metric": metric,
#         "left_entity": {
#             "name": left_entity,
#             **summarize(left_rows)
#         },
#         "right_entity": {
#             "name": right_entity,
#             **summarize(right_rows)
#         }
#     }


# def execute_forecast(
#     demand_df,
#     filters,
#     metric
# ):
#     matched_rows = apply_filters(
#         demand_df,
#         filters
#     )

#     if matched_rows.empty:
#         return {}

#     avg_forecast = round(
#         matched_rows[
#             "forecast_next_30_days"
#         ].mean(),
#         2
#     )

#     return {
#         "query_type": "forecast",
#         "metric": metric,
#         "forecast_next_30_days": avg_forecast
#     }


# # =====================================
# # MAIN ORCHESTRATOR
# # =====================================

# def execute_query_plan(
#     inventory_df,
#     dsl
# ):
#     """
#     Safe Query Executor

#     Orchestrator only.

#     No giant if-elif jungle.
#     """

#     demand_df = load_demand_forecast()

#     inventory_df = inventory_df.copy()

#     inventory_df["category"] = (
#         inventory_df["item_id"]
#         .apply(extract_category)
#     )

#     query_type = dsl.get(
#         "query_type",
#         "fallback"
#     )

#     filters = dsl.get(
#         "filters",
#         {}
#     )

#     metric = dsl.get(
#         "metric",
#         ""
#     )

#     handler_map = {
#         "category_analysis":
#             lambda: execute_category_analysis(
#                 inventory_df,
#                 filters,
#                 metric
#             ),

#         "product_analysis":
#             lambda: execute_product_analysis(
#                 inventory_df,
#                 filters,
#                 metric
#             ),

#         "ranking":
#             lambda: execute_ranking(
#                 inventory_df,
#                 dsl,
#                 metric
#             ),

#         "comparison":
#             lambda: execute_comparison(
#                 inventory_df,
#                 filters,
#                 metric
#             ),

#         "forecast":
#             lambda: execute_forecast(
#                 demand_df,
#                 filters,
#                 metric
#             )
#     }

#     handler = handler_map.get(
#         query_type
#     )

#     if not handler:
#         return fallback_response()

#     return handler()

# query_executor.py

import pandas as pd
import glob


# =====================================
# DATA LOADERS
# =====================================

def load_inventory_data():
    return pd.read_csv(
        "data/gold_inventory_risk.csv"
    )


def load_demand_forecast():
    files = glob.glob(
        "data/gold_demand_forecast/*.csv"
    )

    if not files:
        return pd.DataFrame()

    return pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )


# =====================================
# SHARED HELPERS
# =====================================

def extract_category(item_id):
    if not isinstance(item_id, str):
        return ""

    return item_id.split("_")[0].upper()


def map_metric_column(metric):
    """
    Business metric → real dataframe column
    """

    mapping = {
        "sales": "avg_daily_sales",
        "avg_daily_sales": "avg_daily_sales",
        "inventory_risk": "risk_level",
        "stockout_risk": "risk_level",
        "anomaly_score": "sales_volatility"
    }

    return mapping.get(
        metric,
        "avg_daily_sales"
    )


def risk_level_to_score(value):
    mapping = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    return mapping.get(
        str(value).upper(),
        0
    )


def apply_filters(df, filters):
    """
    Generic filter engine
    """

    result = df.copy()

    for rule in filters:
        field = rule.get(
            "field"
        )

        operator = rule.get(
            "operator"
        )

        value = rule.get(
            "value"
        )

        if field == "category":
            if "category" not in result.columns:
                result["category"] = (
                    result["item_id"]
                    .apply(extract_category)
                )

        if field not in result.columns:
            continue

        if operator == "=":
            result = result[
                result[field]
                .astype(str)
                .str.upper()
                == str(value).upper()
            ]

        elif operator == "startswith":
            result = result[
                result[field]
                .astype(str)
                .str.upper()
                .str.startswith(
                    str(value).upper()
                )
            ]

        elif operator == ">":
            result = result[
                result[field] > value
            ]

        elif operator == "<":
            result = result[
                result[field] < value
            ]

    return result


def fallback_response():
    return {
        "query_type": "fallback",
        "message": (
            "No valid execution path found."
        )
    }


# =====================================
# EXECUTION TYPES
# =====================================

def execute_ranking(
    df,
    dsl
):
    metric = dsl.get(
        "metric",
        "sales"
    )

    mapped_column = (
        map_metric_column(metric)
    )

    if mapped_column == "risk_level":
        df = df.copy()
        df["risk_score"] = (
            df["risk_level"]
            .apply(
                risk_level_to_score
            )
        )
        mapped_column = (
            "risk_score"
        )

    group_by = dsl.get(
        "group_by",
        []
    )

    if not group_by:
        return {}

    group_field = group_by[0]

    grouped = (
        df.groupby(group_field)[
            mapped_column
        ]
        .sum()
        .reset_index(name="score")
    )

    sort_config = dsl.get(
        "sort",
        {}
    )

    sort_order = sort_config.get(
        "order",
        "desc"
    )

    ascending = (
        sort_order == "asc"
    )

    limit = dsl.get(
        "limit",
        5
    )

    grouped = grouped.sort_values(
        by="score",
        ascending=ascending
    ).head(limit)

    return {
        "query_type": "ranking",
        "metric": metric,
        "ranking_results": grouped.to_dict(
            orient="records"
        )
    }


def execute_comparison(
    df,
    dsl
):
    comparison = dsl.get(
        "comparison",
        {}
    )

    left = comparison.get(
        "left",
        ""
    )

    right = comparison.get(
        "right",
        ""
    )

    metric = comparison.get(
        "metric",
        "inventory_risk"
    )

    if "category" not in df.columns:
        df["category"] = (
            df["item_id"]
            .apply(extract_category)
        )

    left_df = df[
        df["category"] == left
    ]

    right_df = df[
        df["category"] == right
    ]

    if left_df.empty or right_df.empty:
        return {}

    def summarize(x):
        return {
            "total_items": len(x),
            "avg_sales": round(
                x["avg_daily_sales"]
                .mean(),
                2
            ),
            "high_risk_count": len(
                x[
                    x["risk_level"]
                    == "HIGH"
                ]
            )
        }

    return {
        "query_type": "comparison",
        "metric": metric,
        "left_entity": {
            "name": left,
            **summarize(left_df)
        },
        "right_entity": {
            "name": right,
            **summarize(right_df)
        }
    }


def execute_forecast(
    df,
    dsl
):
    if df.empty:
        return {}

    avg_forecast = round(
        df[
            "forecast_next_30_days"
        ].mean(),
        2
    )

    return {
        "query_type": "forecast",
        "forecast_next_30_days": avg_forecast
    }


def execute_diagnostic_analysis(
    df,
    dsl
):
    filters = dsl.get(
        "filters",
        []
    )

    item_filter = None

    for f in filters:
        if f.get("field") == "item_id":
            item_filter = f.get(
                "value"
            )

    if item_filter:
        matched = df[
            df["item_id"]
            .str.upper()
            .str.startswith(
                item_filter.upper()
            )
        ]
    else:
        matched = df

    if matched.empty:
        return {}

    high_risk_rows = matched[
        matched["risk_level"]
        == "HIGH"
    ]

    return {
        "query_type": "product_analysis",
        "item_id": matched[
            "item_id"
        ].iloc[0],
        "total_stores": int(
            matched[
                "store_id"
            ].nunique()
        ),
        "avg_daily_sales": round(
            matched[
                "avg_daily_sales"
            ].mean(),
            2
        ),
        "high_risk_store_count": int(
            high_risk_rows[
                "store_id"
            ].nunique()
        ),
        "highest_risk_store": (
            "No high-risk store identified"
            if high_risk_rows.empty
            else high_risk_rows[
                "store_id"
            ].mode()[0]
        ),
        "dominant_risk_level": matched[
            "risk_level"
        ].mode()[0]
    }


# =====================================
# MAIN ORCHESTRATOR
# =====================================

def execute_query_plan(
    inventory_df,
    dsl
):
    """
    Safe analytical engine

    LLM produces DSL only

    Python executes only
    approved operations
    """

    source = dsl.get(
        "source",
        "gold_inventory_risk"
    )

    if source == "gold_demand_forecast":
        df = load_demand_forecast()
    else:
        df = inventory_df.copy()

    if "category" not in df.columns:
        if "item_id" in df.columns:
            df["category"] = (
                df["item_id"]
                .apply(
                    extract_category
                )
            )

    filters = dsl.get(
        "filters",
        []
    )

    df = apply_filters(
        df,
        filters
    )

    if df.empty:
        return {}

    query_type = dsl.get(
        "query_type",
        "fallback"
    )

    handler_map = {
        "ranking":
            execute_ranking,

        "comparison":
            execute_comparison,

        "forecast":
            execute_forecast,

        "diagnostic_analysis":
            execute_diagnostic_analysis
    }

    handler = handler_map.get(
        query_type
    )

    if not handler:
        return fallback_response()

    return handler(
        df,
        dsl
    )