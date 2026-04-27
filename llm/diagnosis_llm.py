# from llm.llm_client import call_llm
# from prompts.diagnosis_prompt import DIAGNOSIS_PROMPT


# def get_diagnosis_from_llm(state) -> str:
#     """
#     Use LLM to determine
#     operational root cause
#     """

#     prompt = DIAGNOSIS_PROMPT.format(
#         item_id=state["item_id"],
#         store_id=state["store_id"],
#         inventory_risk=state["inventory_risk"],
#         price_sensitivity=state["price_sensitivity"],
#         anomaly_flag=state["anomaly_flag"],
#         anomaly_score=state["anomaly_score"]
#     )

#     response = call_llm(prompt)

#     return response

from llm.llm_client import call_llm
from prompts.diagnosis_prompt import DIAGNOSIS_PROMPT


def get_diagnosis_from_llm(state) -> str:
    """
    Use LLM for diagnosis reasoning
    """

    prompt = DIAGNOSIS_PROMPT.format(
        item_id=state.get("item_id", "N/A"),
        store_id=state.get("store_id", "N/A"),
        category=state.get("category", "N/A"),

        inventory_risk=state.get("inventory_risk", "MEDIUM"),
        price_sensitivity=state.get("price_sensitivity", "MEDIUM"),
        anomaly_flag=state.get("anomaly_flag", "MEDIUM"),
        anomaly_score=state.get("anomaly_score", 0),

        total_items=state.get("total_items", 0),
        high_risk_count=state.get("high_risk_count", 0),
        top_store=state.get("top_store", "N/A")
    )

    response = call_llm(prompt)

    return response