# forecasting/inventory_forecast.py

def forecast_stockout_risk(
    current_inventory,
    demand_forecast_output
):
    """
    Predict stockout risk using:

    inventory
    vs
    forecasted demand

    Parameters:
    ----------
    current_inventory : int / float

    demand_forecast_output : dict

    Returns:
    ----------
    dict
    """

    avg_daily_sales = demand_forecast_output.get(
        "avg_daily_sales",
        0
    )

    if avg_daily_sales == 0:
        return {
            "message": "Unable to calculate stockout risk."
        }

    days_to_stockout = (
        current_inventory / avg_daily_sales
    )

    if days_to_stockout < 5:
        risk = "HIGH"

    elif days_to_stockout < 10:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return {
        "days_to_stockout": round(days_to_stockout, 2),
        "stockout_risk": risk,
        "recommended_buffer_days": 14
    }