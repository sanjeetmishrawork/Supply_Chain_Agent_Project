
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


def load_stockout_risk():
    files = glob.glob(
        "data/gold_stockout_risk/*.csv"
    )

    if not files:
        return pd.DataFrame()

    return pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )


def load_price_impact():
    files = glob.glob(
        "data/gold_price_impact/*.csv"
    )

    if not files:
        return pd.DataFrame()

    return pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )


def load_demand_anomaly():
    files = glob.glob(
        "data/gold_demand_anomaly/*.csv"
    )

    if not files:
        return pd.DataFrame()

    return pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )


# =====================================
# HELPERS
# =====================================

def extract_category(item_id):
    if not isinstance(item_id, str):
        return ""

    return item_id.split("_")[0].upper()


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


def map_metric_column(metric):
    mapping = {
        "sales": "avg_daily_sales",
        "avg_daily_sales": "avg_daily_sales",
        "inventory_risk": "risk_level",
        "stockout_risk": "stockout_risk",
        "anomaly_score": "anomaly_score",
        "price_sensitivity": "price_sensitivity_flag",
        "forecast_next_7_days": "forecast_next_7_days",
        "forecast_next_30_days": "forecast_next_30_days",
        "zero_sales_days": "zero_sales_days",
        "sales_volatility": "sales_volatility"
    }

    return mapping.get(
        metric,
        "avg_daily_sales"
    )


def apply_filters(df, filters):
    result = df.copy()

    for rule in filters:
        field = rule.get("field")
        operator = rule.get("operator")
        value = rule.get("value")

        if (
            field == "category"
            and "category" not in result.columns
            and "item_id" in result.columns
        ):
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
                .str.strip()
                .str.upper()
                == str(value).upper()
            ]

        elif operator == "startswith":
            result = result[
                result[field]
                .astype(str)
                .str.strip()
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
        "message": "No valid execution path found."
    }


# =====================================
# DISCOVERY
# =====================================

def execute_discovery(df, dsl):
    target_field = dsl.get(
        "target_field",
        "category"
    )

    if target_field == "schema":
        return {
            "query_type": "discovery",
            "available_fields": list(df.columns)
        }

    if target_field not in df.columns:
        return {
            "query_type": "discovery",
            "target_field": target_field,
            "values": []
        }

    values = sorted(
        df[target_field]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
        .tolist()
    )

    return {
        "query_type": "discovery",
        "target_field": target_field,
        "values": values
    }


# =====================================
# PRODUCT ANALYSIS
# =====================================

def execute_product_analysis(df):
    if df.empty:
        return {}

    high_risk_rows = df[
        df["risk_level"] == "HIGH"
    ]

    return {
        "query_type": "product_analysis",
        "item_id": df["item_id"].iloc[0],
        "total_stores": int(
            df["store_id"].nunique()
        ),
        "avg_daily_sales": round(
            df["avg_daily_sales"].mean(),
            2
        ),
        "dominant_risk_level": df[
            "risk_level"
        ].mode()[0],
        "high_risk_store_count": int(
            high_risk_rows["store_id"].nunique()
        )
    }


# =====================================
# CATEGORY ANALYSIS
# =====================================

def execute_category_analysis(df):
    if df.empty:
        return {}

    high_risk_rows = df[
        df["risk_level"] == "HIGH"
    ]

    return {
        "query_type": "category_analysis",
        "category": df["category"].iloc[0],
        "total_items": int(
            df["item_id"].nunique()
        ),
        "avg_daily_sales": round(
            df["avg_daily_sales"].mean(),
            2
        ),
        "high_risk_count": int(
            high_risk_rows["item_id"].nunique()
        ),
        "top_store": df[
            "store_id"
        ].mode()[0]
    }


# =====================================
# STORE ANALYSIS
# =====================================

def execute_store_analysis(df):
    if df.empty:
        return {}

    high_risk_rows = df[
        df["risk_level"] == "HIGH"
    ]

    return {
        "query_type": "store_analysis",
        "store_id": df["store_id"].iloc[0],
        "total_products": int(
            df["item_id"].nunique()
        ),
        "avg_daily_sales": round(
            df["avg_daily_sales"].mean(),
            2
        ),
        "high_risk_products": int(
            high_risk_rows["item_id"].nunique()
        ),
        "top_category": df[
            "category"
        ].mode()[0]
    }


# =====================================
# DEPARTMENT ANALYSIS
# =====================================

def execute_department_analysis(df):
    if df.empty:
        return {}

    high_risk_rows = df[
        df["risk_level"] == "HIGH"
    ]

    return {
        "query_type": "department_analysis",
        "department": df["department"].iloc[0],
        "total_items": int(
            df["item_id"].nunique()
        ),
        "avg_daily_sales": round(
            df["avg_daily_sales"].mean(),
            2
        ),
        "high_risk_count": int(
            high_risk_rows["item_id"].nunique()
        )
    }


# =====================================
# STATE ANALYSIS
# =====================================

def execute_state_analysis(df):
    if df.empty:
        return {}

    high_risk_rows = df[
        df["risk_level"] == "HIGH"
    ]

    return {
        "query_type": "state_analysis",
        "state_id": df["state_id"].iloc[0],
        "total_items": int(
            df["item_id"].nunique()
        ),
        "avg_daily_sales": round(
            df["avg_daily_sales"].mean(),
            2
        ),
        "high_risk_count": int(
            high_risk_rows["item_id"].nunique()
        ),
        "top_category": df[
            "category"
        ].mode()[0]
    }


# =====================================
# RANKING
# =====================================

def execute_ranking(df, dsl):
    metric = dsl.get(
        "metric",
        "sales"
    )

    mapped_column = map_metric_column(metric)

    if mapped_column == "risk_level":
        df = df.copy()
        df["risk_score"] = (
            df["risk_level"]
            .apply(risk_level_to_score)
        )
        mapped_column = "risk_score"

    group_by = dsl.get(
        "group_by",
        []
    )

    if not group_by:
        return {}

    group_field = group_by[0]

    grouped = (
        df.groupby(group_field)[mapped_column]
        .sum()
        .reset_index(name="score")
    )

    sort_config = dsl.get(
        "sort",
        {}
    )

    ascending = (
        sort_config.get(
            "order",
            "desc"
        ) == "asc"
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


# =====================================
# THRESHOLD
# =====================================

def execute_threshold(df, dsl):
    metric = dsl.get(
        "metric",
        "zero_sales_days"
    )

    threshold = dsl.get(
        "threshold",
        None
    )

    if threshold is None:
        return {}

    mapped_column = map_metric_column(metric)

    if mapped_column not in df.columns:
        return {}

    if mapped_column == "risk_level":
        return {}

    filtered = df[
        df[mapped_column] > threshold
    ].copy()

    if filtered.empty:
        return {}

    entity_field = "item_id"

    if dsl.get("entity_type") == "store_id":
        entity_field = "store_id"

    elif dsl.get("entity_type") == "category":
        entity_field = "category"

    elif dsl.get("entity_type") == "department":
        entity_field = "department"

    elif dsl.get("entity_type") == "state_id":
        entity_field = "state_id"

    grouped = (
        filtered
        .groupby(entity_field)[mapped_column]
        .mean()
        .reset_index(name="score")
        .sort_values(
            by="score",
            ascending=False
        )
        .head(
            dsl.get("limit", 10)
        )
    )

    return {
        "query_type": "threshold",
        "metric": metric,
        "threshold": threshold,
        "ranking_results": grouped.to_dict(
            orient="records"
        )
    }


# =====================================
# COMPARISON
# =====================================

def execute_comparison(df, dsl):
    comparison = dsl.get(
        "comparison",
        {}
    )

    left = comparison.get("left", "")
    right = comparison.get("right", "")
    metric = comparison.get(
        "metric",
        "inventory_risk"
    )

    if "category" not in df.columns:
        return {}

    left_df = df[
        df["category"]
        .astype(str)
        .str.strip()
        .str.upper()
        == left.upper()
    ]

    right_df = df[
        df["category"]
        .astype(str)
        .str.strip()
        .str.upper()
        == right.upper()
    ]

    if left_df.empty or right_df.empty:
        return {}

    def summarize(x):
        return {
            "total_items": int(
                x["item_id"].nunique()
            ),
            "avg_daily_sales": round(
                x["avg_daily_sales"].mean(),
                2
            ),
            "high_risk_count": int(
                x[
                    x["risk_level"] == "HIGH"
                ]["item_id"].nunique()
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


# =====================================
# FORECAST
# =====================================

def execute_forecast(df):
    if df.empty:
        return {}

    return {
        "query_type": "forecast",
        "forecast_next_30_days": round(
            df[
                "forecast_next_30_days"
            ].mean(),
            2
        )
    }


# =====================================
# MAIN EXECUTOR
# =====================================

def execute_query_plan(
    inventory_df,
    dsl
):
    source = dsl.get(
        "source",
        "gold_inventory_risk"
    )

    if source == "gold_demand_forecast":
        df = load_demand_forecast()

    elif source == "gold_stockout_risk":
        df = load_stockout_risk()

    elif source == "gold_price_impact":
        df = load_price_impact()

    elif source == "gold_demand_anomaly":
        df = load_demand_anomaly()

    else:
        df = inventory_df.copy()

    if df.empty:
        return {}

    query_type = dsl.get(
        "query_type",
        "fallback"
    )

    if query_type == "comparison":
        return execute_comparison(
            df,
            dsl
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

    if query_type == "diagnostic_analysis":

        if any(
            f.get("field") == "item_id"
            for f in filters
        ):
            return execute_product_analysis(df)

        elif any(
            f.get("field") == "category"
            for f in filters
        ):
            return execute_category_analysis(df)

        elif any(
            f.get("field") == "department"
            for f in filters
        ):
            return execute_department_analysis(df)

        elif any(
            f.get("field") == "store_id"
            for f in filters
        ):
            return execute_store_analysis(df)

        elif any(
            f.get("field") == "state_id"
            for f in filters
        ):
            return execute_state_analysis(df)

        else:
            return fallback_response()

    handler_map = {
        "discovery": execute_discovery,
        "ranking": execute_ranking,
        "forecast": execute_forecast,
        "threshold": execute_threshold
    }

    handler = handler_map.get(
        query_type
    )

    if not handler:
        return fallback_response()

    if query_type == "forecast":
        return handler(df)

    return handler(
        df,
        dsl
    )
