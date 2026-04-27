# llm/reflection_llm.py

from llm.llm_client import call_llm
from prompts.reflection_prompt import get_reflection_prompt


def run_reflection_llm(
    user_input,
    failure_stage,
    actual_failure_reason,
    planner_output,
    validation_output,
    execution_result
):
    """
    Reflection LLM Execution Layer

    Purpose:
    Analyze failures using
    explicit code-detected diagnosis.

    IMPORTANT:
    This does NOT answer
    the business question.

    This improves:
    planner quality
    validation discipline
    system reliability

    This is:
    reflection based on facts,
    not LLM guessing.

    Output Example:

    Failure Cause:
    Validator over-rejected
    comparison query

    Why It Happened:
    Placeholder fields created ambiguity

    Suggested Improvement:
    Remove unnecessary fields

    Future Prompt Rule:
    Only include limit for ranking queries
    """

    prompt = get_reflection_prompt(
        user_input=user_input,
        failure_stage=failure_stage,
        actual_failure_reason=actual_failure_reason,
        planner_output=planner_output,
        validation_output=validation_output,
        execution_result=execution_result
    )

    print(
        "\n--- Calling Reflection LLM ---\n"
    )

    response = call_llm(prompt)

    print(
        "Reflection LLM Response:\n"
    )
    print(response)

    print(
        "\n-----------------------------------\n"
    )

    return response