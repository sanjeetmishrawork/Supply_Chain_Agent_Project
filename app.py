import pandas as pd
import glob

from graph import build_graph


def load_price_signal():
    """
    Read multiple CSV part files from:
    data/gold_price_impact/
    and determine a simple price sensitivity signal.
    """

    files = glob.glob("data/gold_price_impact/*.csv")

    if not files:
        return "MEDIUM"

    df = pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )

    if "price_sensitivity_flag" in df.columns:
        high_count = (df["price_sensitivity_flag"] == "HIGH").sum()

        if high_count > 0:
            return "HIGH"

    return "MEDIUM"


def load_anomaly_signal():
    """
    Read multiple CSV part files from:
    data/gold_demand_anomaly/
    and return anomaly severity.
    """

    files = glob.glob("data/gold_demand_anomaly/*.csv")

    if not files:
        return ("MEDIUM", 5.0)

    df = pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )

    if "anomaly_score" in df.columns:
        max_score = float(df["anomaly_score"].max())

        if max_score > 5:
            return ("HIGH", max_score)

        return ("MEDIUM", max_score)

    return ("MEDIUM", 5.0)


def main():
    """
    Execute full LangGraph agent workflow
    """

    # Read inventory risk CSV
    inventory_df = pd.read_csv(
        "data/gold_inventory_risk.csv"
    )

    # Take first HIGH risk row for demo execution
    high_risk_rows = inventory_df[
        inventory_df["risk_level"] == "HIGH"
    ]

    if high_risk_rows.empty:
        print("No HIGH risk items found.")
        return

    selected_row = high_risk_rows.iloc[0]

    item_id = selected_row["item_id"]
    store_id = selected_row["store_id"]
    inventory_risk = selected_row["risk_level"]

    # Load supporting signals
    price_sensitivity = load_price_signal()
    anomaly_flag, anomaly_score = load_anomaly_signal()

    # Initial LangGraph state
    initial_state = {
        "item_id": item_id,
        "store_id": store_id,

        "inventory_risk": inventory_risk,
        "price_sensitivity": price_sensitivity,
        "anomaly_flag": anomaly_flag,
        "anomaly_score": anomaly_score,

        "anomaly_signal": "",
        "root_cause": "",
        "recommended_action": "",
        "business_impact": "",
        "executive_summary": "",

        "confidence_score": 0.0
    }

    # Build graph
    app = build_graph()

    # Run workflow
    final_state = app.invoke(initial_state)

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(final_state["executive_summary"])
    print("\n=======================================\n")


if __name__ == "__main__":
    main()