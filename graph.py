from langgraph.graph import StateGraph, END

from state import AgentState

from agents.detection import detection_agent
from agents.diagnosis import diagnosis_agent
from agents.recommendation import recommendation_agent
from agents.strategy import strategy_agent
from agents.summary import summary_agent


def build_graph():
    """
    Build LangGraph multi-agent workflow

    Flow:
    START
    → Detection
    → Diagnosis
    → Recommendation
    → Strategy
    → Summary
    → END
    """

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("detection", detection_agent)
    workflow.add_node("diagnosis", diagnosis_agent)
    workflow.add_node("recommendation", recommendation_agent)
    workflow.add_node("strategy", strategy_agent)
    workflow.add_node("summary", summary_agent)

    # Set entry point
    workflow.set_entry_point("detection")

    # Define flow
    workflow.add_edge("detection", "diagnosis")
    workflow.add_edge("diagnosis", "recommendation")
    workflow.add_edge("recommendation", "strategy")
    workflow.add_edge("strategy", "summary")
    workflow.add_edge("summary", END)

    # Compile graph
    app = workflow.compile()

    return app