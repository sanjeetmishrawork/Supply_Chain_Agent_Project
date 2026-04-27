# llm/validator_llm.py

from llm.llm_client import call_llm
from prompts.validator_prompt import get_validator_prompt


def run_validator_llm(query_plan):
    """
    Validator LLM Execution Layer

    Purpose:
    Validate whether the planner-generated
    query plan is executable,
    logically correct,
    and safe.

    IMPORTANT:
    This does NOT answer the business question.

    This only checks whether
    the plan deserves execution.

    Output Example:

    {
        "is_valid": true,
        "issues": [],
        "suggested_fix": ""
    }

    OR

    {
        "is_valid": false,
        "issues": [
            "Metric is invalid"
        ],
        "suggested_fix": "Use approved metrics only"
    }

    This prevents confident nonsense
    from reaching production.
    """

    prompt = get_validator_prompt(
        query_plan
    )

    print(
        "\n--- Calling Validator LLM ---\n"
    )

    response = call_llm(prompt)

    print(
        "Validator LLM Raw Response:\n"
    )
    print(response)

    print(
        "\n-----------------------------------\n"
    )

    return response