# from state import AgentState


# def diagnosis_agent(state: AgentState) -> AgentState:
#     """
#     Diagnosis Agent

#     Purpose:
#     Identify the most likely root cause using:
#     - anomaly signal
#     - price sensitivity
#     - inventory risk
#     """

#     inventory_risk = state["inventory_risk"]
#     price_sensitivity = state["price_sensitivity"]
#     anomaly_flag = state["anomaly_flag"]

#     # Rule-based diagnosis logic (Version 1)
#     if (
#         inventory_risk == "HIGH"
#         and anomaly_flag == "HIGH"
#         and price_sensitivity == "HIGH"
#     ):
#         state["root_cause"] = (
#             "Promotion-driven demand spike causing stockout risk."
#         )

#     elif (
#         inventory_risk == "HIGH"
#         and anomaly_flag == "HIGH"
#     ):
#         state["root_cause"] = (
#             "Sudden demand surge creating replenishment pressure."
#         )

#     elif price_sensitivity == "HIGH":
#         state["root_cause"] = (
#             "Pricing strategy is strongly influencing demand."
#         )

#     else:
#         state["root_cause"] = (
#             "Demand instability likely caused by normal sales variation."
#         )

#     return state

from state import AgentState
from llm.diagnosis_llm import get_diagnosis_from_llm


def diagnosis_agent(state: AgentState) -> AgentState:
    """
    Diagnosis Agent
    """

    try:
        print("\n--- Calling LLM for Diagnosis ---\n")

        root_cause = get_diagnosis_from_llm(state)

        print("LLM Response:", root_cause)

        state["root_cause"] = root_cause

    except Exception as e:
        print("LLM ERROR:", str(e))

        state["root_cause"] = (
            f"LLM diagnosis failed. Error: {str(e)}"
        )

    return state