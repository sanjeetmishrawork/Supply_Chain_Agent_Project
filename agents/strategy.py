# from state import AgentState


# def strategy_agent(state: AgentState) -> AgentState:
#     """
#     Strategy Agent

#     Purpose:
#     Estimate likely business and financial impact
#     based on recommendation and severity.
#     """

#     recommended_action = state["recommended_action"]
#     confidence_score = state["confidence_score"]
#     anomaly_score = state["anomaly_score"]

#     # Simple impact estimation logic (Version 1)
#     if "safety stock" in recommended_action.lower():
#         state["business_impact"] = (
#             f"Potential stockout prevention with high urgency. "
#             f"Estimated avoided revenue loss: ${int(anomaly_score * 25000)}."
#         )

#     elif "pricing strategy" in recommended_action.lower():
#         state["business_impact"] = (
#             f"Potential pricing optimization opportunity. "
#             f"Estimated margin protection: ${int(anomaly_score * 18000)}."
#         )

#     elif "replenishment" in recommended_action.lower():
#         state["business_impact"] = (
#             f"Improved supply continuity expected. "
#             f"Estimated operational efficiency gain: ${int(anomaly_score * 15000)}."
#         )

#     else:
#         state["business_impact"] = (
#             f"Moderate operational improvement expected. "
#             f"Estimated impact: ${int(anomaly_score * 10000)}."
#         )

#     return state

from state import AgentState
from llm.strategy_llm import get_strategy_from_llm


def strategy_agent(state: AgentState) -> AgentState:
    """
    Strategy Agent

    Purpose:
    Estimate business impact and urgency
    using LLM reasoning.
    """

    try:
        print("\n--- Calling LLM for Strategy ---\n")

        strategy_output = get_strategy_from_llm(state)

        print("LLM Strategy:", strategy_output)

        state["business_impact"] = strategy_output

    except Exception as e:
        print("LLM Strategy ERROR:", str(e))

        state["business_impact"] = (
            f"Strategy generation failed. Error: {str(e)}"
        )

    return state