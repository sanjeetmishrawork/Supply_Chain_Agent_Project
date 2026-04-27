# llm/planner_llm.py

from llm.llm_client import call_llm
from prompts.planner_prompt import get_planner_prompt


def run_planner_llm(user_input):
    """
    Planner LLM Execution Layer

    Purpose:
    Send user query into the planner prompt
    and retrieve:

    1. Reasoning Steps
    2. Final Query Plan

    IMPORTANT:
    This does NOT answer the business question.

    This only creates the execution strategy.

    Output example:

    Reasoning Steps:
    1. User asks ranking query
    2. Entity is store
    3. Metric is stockout risk

    Final Query Plan:
    {
        ...
    }

    This creates visible intelligence.
    """

    prompt = get_planner_prompt(
        user_input
    )

    print(
        "\n--- Calling Planner LLM ---\n"
    )

    response = call_llm(prompt)

    print(
        "Planner LLM Raw Response:\n"
    )
    print(response)

    print(
        "\n-----------------------------------\n"
    )

    return response