# llm/repair_llm.py

from llm.llm_client import call_llm
from prompts.repair_prompt import get_repair_prompt


def run_repair_llm(
    user_input,
    query_plan,
    validation_result
):
    """
    Repair LLM Execution Layer

    Purpose:
    Generate minimal safe JSON patch
    for invalid query plans.

    IMPORTANT:

    This is NOT re-planning.

    This is NOT reasoning.

    This is NOT business advice.

    This is:

    validator-driven repair.

    Expected Output:

    Example:

    {
        "metric": "inventory_risk"
    }

    or

    {
        "aggregation": "top",
        "limit": 5
    }

    Only patch.
    Nothing else.
    """

    prompt = get_repair_prompt(
        user_input=user_input,
        query_plan=query_plan,
        validation_result=validation_result
    )

    print(
        "\n--- Calling Repair LLM ---\n"
    )

    raw_response = call_llm(
        prompt
    )

    print(
        "Repair LLM Raw Response:\n"
    )
    print(raw_response)

    print(
        "\n-----------------------------------\n"
    )

    return raw_response
