# agents/prompt_planner.py

import json
import re

from llm.planner_llm import run_planner_llm


def extract_json_block(text):
    """
    Extract JSON safely from LLM output

    Because LLMs enjoy wrapping JSON
    inside unnecessary poetry.

    We remove the drama.
    """

    try:
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if match:
            return match.group()

        return None

    except Exception:
        return None


def extract_reasoning_steps(text):
    """
    Extract reasoning steps section

    Example:

    Reasoning Steps:
    1. User asks ranking query
    2. Entity is store
    """

    lines = text.split("\n")

    steps = []

    capture = False

    for line in lines:
        line = line.strip()

        if "Reasoning Steps" in line:
            capture = True
            continue

        if "Final Query Plan" in line:
            break

        if capture and line:
            steps.append(line)

    return steps


def plan_user_query(user_input):
    """
    Prompt Planning Agent

    Purpose:
    Convert user question into:

    1. Visible reasoning steps
    2. Structured query plan

    Output:

    {
        "reasoning_steps": [...],
        "query_plan": {...}
    }

    This is:
    LLM decides WHAT
    system decides HOW
    """

    raw_response = run_planner_llm(
        user_input
    )

    reasoning_steps = extract_reasoning_steps(
        raw_response
    )

    json_block = extract_json_block(
        raw_response
    )

    if not json_block:
        print(
            "\nPlanner failed to produce JSON.\n"
        )

        return {
            "reasoning_steps": reasoning_steps,
            "query_plan": {
                "intent": "executive_summary",
                "entity_type": "none",
                "reasoning_hint": "fallback route"
            }
        }

    try:
        parsed_plan = json.loads(
            json_block
        )

        print(
            "\nStructured Query Plan:\n"
        )
        print(parsed_plan)

        return {
            "reasoning_steps": reasoning_steps,
            "query_plan": parsed_plan
        }

    except Exception as e:
        print(
            "\nPlanner JSON parsing failed:",
            str(e)
        )

        return {
            "reasoning_steps": reasoning_steps,
            "query_plan": {
                "intent": "executive_summary",
                "entity_type": "none",
                "reasoning_hint": "fallback route"
            }
        }
    


def planner_agent(state):
    """
    LangGraph wrapper for planner agent

    Converts:
    user_input
    →

    query_plan
    + reasoning_steps

    This keeps existing planner logic
    and makes it compatible with LangGraph.
    """

    user_input = state.get(
        "user_input",
        ""
    )

    planner_result = plan_user_query(
        user_input
    )

    state["query_plan"] = planner_result.get(
        "query_plan",
        {}
    )

    state["planner_reasoning"] = "\n".join(
        planner_result.get(
            "reasoning_steps",
            []
        )
    )

    return state
