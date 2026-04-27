from state import AgentState


def detection_agent(state: AgentState) -> AgentState:
    """
    Detection Agent

    Purpose:
    Identify the primary anomaly signal using
    inventory risk + anomaly severity.
    """

    inventory_risk = state["inventory_risk"]
    anomaly_flag = state["anomaly_flag"]
    anomaly_score = state["anomaly_score"]

    # Rule-based detection logic (Version 1)
    if inventory_risk == "HIGH" and anomaly_flag == "HIGH":
        state["anomaly_signal"] = (
            f"Critical operational anomaly detected "
            f"(score: {anomaly_score}) with high inventory risk."
        )

    elif anomaly_flag == "HIGH":
        state["anomaly_signal"] = (
            f"Major sales anomaly detected "
            f"(score: {anomaly_score})."
        )

    elif inventory_risk == "HIGH":
        state["anomaly_signal"] = (
            "High inventory instability detected."
        )

    else:
        state["anomaly_signal"] = (
            "Moderate operational variation detected."
        )

    return state