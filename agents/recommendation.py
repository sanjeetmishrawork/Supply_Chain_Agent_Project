# from state import AgentState


# def recommendation_agent(state: AgentState) -> AgentState:
#     """
#     Recommendation Agent

#     Purpose:
#     Generate the best operational action
#     based on identified root cause.
#     """

#     root_cause = state["root_cause"]

#     # Rule-based recommendation logic (Version 1)
#     if "stockout risk" in root_cause.lower():
#         state["recommended_action"] = (
#             "Increase safety stock and raise reorder frequency immediately."
#         )
#         state["confidence_score"] = 0.90

#     elif "pricing" in root_cause.lower():
#         state["recommended_action"] = (
#             "Review pricing strategy and evaluate promotion effectiveness."
#         )
#         state["confidence_score"] = 0.80

#     elif "demand surge" in root_cause.lower():
#         state["recommended_action"] = (
#             "Adjust replenishment thresholds and accelerate supply planning."
#         )
#         state["confidence_score"] = 0.85

#     else:
#         state["recommended_action"] = (
#             "Review forecasting assumptions and monitor demand continuity."
#         )
#         state["confidence_score"] = 0.70

#     return state

from state import AgentState
from llm.recommendation_llm import get_recommendation_from_llm


def recommendation_agent(state: AgentState) -> AgentState:
    """
    Recommendation Agent

    Purpose:
    Use LLM reasoning to determine
    the best operational action.
    """

    try:
        print("\n--- Calling LLM for Recommendation ---\n")

        recommendation = get_recommendation_from_llm(state)

        print("LLM Recommendation:", recommendation)

        state["recommended_action"] = recommendation

    except Exception as e:
        print("LLM Recommendation ERROR:", str(e))

        state["recommended_action"] = (
            f"Recommendation generation failed. Error: {str(e)}"
        )

    return state