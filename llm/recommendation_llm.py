# from llm.llm_client import call_llm
# from prompts.recommendation_prompt import RECOMMENDATION_PROMPT


# def get_recommendation_from_llm(state) -> str:
#     prompt = RECOMMENDATION_PROMPT.format(
#         item_id=state["item_id"],
#         store_id=state["store_id"],
#         root_cause=state["root_cause"],
#         inventory_risk=state["inventory_risk"],
#         price_sensitivity=state["price_sensitivity"],
#         anomaly_score=state["anomaly_score"]
#     )

#     return call_llm(prompt)

from llm.llm_client import call_llm
from prompts.recommendation_prompt import RECOMMENDATION_PROMPT


def get_recommendation_from_llm(state) -> str:
    prompt = RECOMMENDATION_PROMPT.format(
        item_id=state.get("item_id", "N/A"),
        store_id=state.get("store_id", "N/A"),
        category=state.get("category", "N/A"),

        root_cause=state.get("root_cause", "N/A"),

        inventory_risk=state.get("inventory_risk", "MEDIUM"),
        price_sensitivity=state.get("price_sensitivity", "MEDIUM"),
        anomaly_score=state.get("anomaly_score", 0),

        total_items=state.get("total_items", 0),
        high_risk_count=state.get("high_risk_count", 0),
        top_store=state.get("top_store", "N/A")
    )

    return call_llm(prompt)