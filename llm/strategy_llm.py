

# from llm.llm_client import call_llm
# from prompts.strategy_prompt import STRATEGY_PROMPT


# def get_strategy_from_llm(state) -> str:
#     prompt = STRATEGY_PROMPT.format(
#         item_id=state["item_id"],
#         store_id=state["store_id"],
#         root_cause=state["root_cause"],
#         recommended_action=state["recommended_action"],
#         anomaly_score=state["anomaly_score"]
#     )

#     return call_llm(prompt)

from llm.llm_client import call_llm
from prompts.strategy_prompt import STRATEGY_PROMPT


def get_strategy_from_llm(state) -> str:
    prompt = STRATEGY_PROMPT.format(
        item_id=state.get("item_id", "N/A"),
        store_id=state.get("store_id", "N/A"),
        category=state.get("category", "N/A"),

        root_cause=state.get("root_cause", "N/A"),
        recommended_action=state.get("recommended_action", "N/A"),

        total_items=state.get("total_items", 0),
        high_risk_count=state.get("high_risk_count", 0),
        top_store=state.get("top_store", "N/A"),

        anomaly_score=state.get("anomaly_score", 0)
    )

    return call_llm(prompt)