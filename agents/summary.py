# from state import AgentState


# def summary_agent(state: AgentState) -> AgentState:
#     """
#     Executive Summary Agent

#     Purpose:
#     Create a leadership-ready summary
#     combining all prior agent outputs.
#     """

#     item_id = state["item_id"]
#     store_id = state["store_id"]

#     anomaly_signal = state["anomaly_signal"]
#     root_cause = state["root_cause"]
#     recommended_action = state["recommended_action"]
#     business_impact = state["business_impact"]
#     confidence_score = state["confidence_score"]

#     state["executive_summary"] = (
#         f"Item {item_id} at Store {store_id} requires immediate review. "
#         f"{anomaly_signal} "
#         f"Likely root cause: {root_cause} "
#         f"Recommended action: {recommended_action} "
#         f"Business impact: {business_impact} "
#         f"Confidence Score: {int(confidence_score * 100)}%."
#     )

#     return state

from state import AgentState
from llm.summary_llm import get_summary_from_llm


def summary_agent(state: AgentState) -> AgentState:
    """
    Summary Agent

    Purpose:
    Generate executive-ready final summary
    using LLM reasoning.
    """

    try:
        print("\n--- Calling LLM for Executive Summary ---\n")

        summary_output = get_summary_from_llm(state)

        print("LLM Summary:", summary_output)

        state["executive_summary"] = summary_output

    except Exception as e:
        print("LLM Summary ERROR:", str(e))

        state["executive_summary"] = (
            f"Executive summary generation failed. Error: {str(e)}"
        )

    return state