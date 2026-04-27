# forecasting/demand_forecast.py

import pandas as pd


def forecast_demand(
    sales_df,
    item_id=None,
    category=None,
    store_id=None,
    horizon_days=30
):
    """
    Flexible demand forecasting function

    Supports:
    - Product level forecasting
    - Category level forecasting
    - Store level forecasting
    - Category + Store forecasting

    Baseline model:
    Rolling average / moving average

    Parameters:
    ----------
    sales_df : pd.DataFrame

    item_id : str
    category : str
    store_id : str
    horizon_days : int

    Returns:
    ----------
    dict
    """

    df = sales_df.copy()

    # -----------------------------------
    # Apply Filters
    # -----------------------------------

    if item_id:
        df = df[
            df["item_id"].str.upper() == item_id.upper()
        ]

    if category:
        df = df[
            df["item_id"].str.upper().str.startswith(
                category.upper()
            )
        ]

    if store_id:
        df = df[
            df["store_id"].str.upper() == store_id.upper()
        ]

    if df.empty:
        return {
            "message": "No matching sales data found."
        }

    # -----------------------------------
    # Basic Forecast Logic
    # -----------------------------------

    # Use last 30 observations
    recent_sales = df.tail(30)

    avg_daily_sales = recent_sales["sales_qty"].mean()

    forecast_total = avg_daily_sales * horizon_days

    peak_sales = recent_sales["sales_qty"].max()

    return {
        "item_id": item_id or "MULTI",
        "category": category or "N/A",
        "store_id": store_id or "N/A",
        "avg_daily_sales": round(avg_daily_sales, 2),
        "forecast_horizon_days": horizon_days,
        "forecast_total_demand": round(forecast_total, 2),
        "peak_recent_sales": round(peak_sales, 2)
    }