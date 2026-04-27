
from langgraph.graph import StateGraph, END

from state import AgentState

from agents.prompt_planner import planner_agent
from agents.validation_agent import validation_agent
from agents.self_healing_agent import self_healing_agent
from agents.reasoning_agent import reasoning_agent
from agents.reflection_agent import reflection_agent

from query_dsl_builder import build_query_dsl
from query_executor import execute_query_plan

from llm.summary_llm import get_summary_from_llm


# =====================================
# DSL Builder Node
# =====================================

def dsl_builder_agent(state):
    """
    Convert validated query plan
    into executable DSL
    """

    active_query_plan = (
        state.get("repaired_query_plan")
        or state.get("query_plan")
    )

    dsl = build_query_dsl(
        active_query_plan
    )

    state["dsl"] = dsl

    return state


# =====================================
# Executor Node
# =====================================

def executor_agent(state):
    """
    Execute DSL query
    against gold tables
    """

    import pandas as pd

    inventory_df = pd.read_csv(
        "data/gold_inventory_risk.csv"
    )

    execution_result = execute_query_plan(
        inventory_df,
        state["dsl"]
    )

    if not execution_result:
        state["failure_stage"] = "execution"
        state["actual_failure_reason"] = (
            "Query execution returned no results"
        )

    state["execution_result"] = execution_result

    return state


# =====================================
# Summary Node
# =====================================

def summary_agent(state):
    """
    Convert reasoning context
    into executive summary
    """

    summary = get_summary_from_llm(
        state.get(
            "reasoning_context",
            ""
        )
    )

    state["final_response"] = summary

    return state


# =====================================
# Validation Router
# =====================================

def validation_router(state):
    """
    Route after validation

    If validation passes:
    continue to DSL

    If validation fails:
    go to repair
    """

    validation_result = state.get(
        "validation_result",
        {}
    )

    if validation_result.get(
        "is_valid",
        False
    ):
        return "dsl_builder"

    return "self_healing"


# =====================================
# Repair Router
# =====================================

def repair_router(state):
    """
    Route after repair

    If repair successful:
    continue

    If repair failed:
    reflection
    """

    repaired = state.get(
        "repaired_query_plan",
        {}
    )

    if repaired:
        return "dsl_builder"

    return "reflection"


# =====================================
# Execution Router
# =====================================

def execution_router(state):
    """
    Route after execution

    Success → reasoning

    Failure → reflection
    """

    if state.get("failure_stage"):
        return "reflection"

    return "reasoning"


# =====================================
# Build Graph
# =====================================

def build_graph():
    """
    Production LangGraph pipeline

    planner
    → validator
    → repair (if needed)
    → DSL builder
    → executor
    → reasoning
    → summary
    → reflection (on failure)
    """

    workflow = StateGraph(
        AgentState
    )

    # Core nodes

    workflow.add_node(
        "planner",
        planner_agent
    )

    workflow.add_node(
        "validator",
        validation_agent
    )

    workflow.add_node(
        "self_healing",
        self_healing_agent
    )

    workflow.add_node(
        "dsl_builder",
        dsl_builder_agent
    )

    workflow.add_node(
        "executor",
        executor_agent
    )

    workflow.add_node(
        "reasoning",
        reasoning_agent
    )

    workflow.add_node(
        "summary",
        summary_agent
    )

    workflow.add_node(
        "reflection",
        reflection_agent
    )

    # Entry point

    workflow.set_entry_point(
        "planner"
    )

    # Flow

    workflow.add_edge(
        "planner",
        "validator"
    )

    workflow.add_conditional_edges(
        "validator",
        validation_router
    )

    workflow.add_conditional_edges(
        "self_healing",
        repair_router
    )

    workflow.add_edge(
        "dsl_builder",
        "executor"
    )

    workflow.add_conditional_edges(
        "executor",
        execution_router
    )

    workflow.add_edge(
        "reasoning",
        "summary"
    )

    workflow.add_edge(
        "summary",
        END
    )

    workflow.add_edge(
        "reflection",
        END
    )

    app = workflow.compile()

    return app
