
from typing import TypedDict


class AgentState(TypedDict):
    """
    Shared LangGraph state across all agents

    This supports the full
    planner → validator → repair
    → DSL → execution → reasoning
    → summary → reflection pipeline
    """

    # -----------------------------------
    # User Input
    # -----------------------------------

    user_input: str

    # -----------------------------------
    # Planning Layer
    # -----------------------------------

    query_plan: dict
    planner_reasoning: str

    # -----------------------------------
    # Validation Layer
    # -----------------------------------

    validation_result: dict
    repaired_query_plan: dict

    # -----------------------------------
    # Execution Layer
    # -----------------------------------

    dsl: dict
    execution_result: dict

    # -----------------------------------
    # Reasoning + Final Output
    # -----------------------------------

    reasoning_context: str
    final_response: str

    # -----------------------------------
    # Failure + Reflection
    # -----------------------------------

    failure_stage: str
    actual_failure_reason: str
    reflection_output: str

    # -----------------------------------
    # Metadata
    # -----------------------------------

    confidence_score: float
