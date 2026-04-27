# from typing import TypedDict


# class AgentState(TypedDict):
#     """
#     Shared state across all LangGraph agents.
#     Every node reads from this and updates this.
#     """

#     # Core identifiers
#     item_id: str
#     store_id: str

#     # Signals from Gold layer
#     inventory_risk: str
#     price_sensitivity: str
#     anomaly_flag: str
#     anomaly_score: float

#     # Agent outputs
#     anomaly_signal: str
#     root_cause: str
#     recommended_action: str
#     business_impact: str
#     executive_summary: str

#     # Confidence / metadata
#     confidence_score: float

from typing import TypedDict


class AgentState(TypedDict):
    """
    Shared LangGraph state across all agents
    """

    # ----------------------------
    # Core Entity Information
    # ----------------------------

    item_id: str
    store_id: str
    category: str

    # ----------------------------
    # Inventory + Risk Signals
    # ----------------------------

    inventory_risk: str
    price_sensitivity: str
    anomaly_flag: str
    anomaly_score: float

    # ----------------------------
    # Aggregated Context
    # ----------------------------

    total_items: int
    high_risk_count: int
    top_store: str

    # ----------------------------
    # Agent Outputs
    # ----------------------------

    anomaly_signal: str
    root_cause: str
    recommended_action: str
    business_impact: str
    executive_summary: str

    # ----------------------------
    # Confidence / Metadata
    # ----------------------------

    confidence_score: float