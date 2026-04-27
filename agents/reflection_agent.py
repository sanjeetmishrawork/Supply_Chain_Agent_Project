# agents/reflection_agent.py

from llm.reflection_llm import run_reflection_llm


def reflect_on_failure(
    user_input,
    failure_stage,
    actual_failure_reason,
    planner_output,
    validation_output,
    execution_result
):
    """
    Reflection Agent

    Purpose:
    Convert failures into
    structured learning signals.

    IMPORTANT:
    Failure diagnosis comes from code,
    not from LLM guessing.

    This creates:
    reliable system improvement.

    Supported failure cases:

    - weak entity extraction
    - wrong intent classification
    - validator over-rejection
    - invalid metric selection
    - empty query results
    - weak business reasoning
    - forecasting interpretation gaps

    This does NOT auto-edit prompts.

    It creates:
    controlled reflection
    for human-guided improvement.
    """

    print(
        "\n========== REFLECTION AGENT ==========\n"
    )

    print(
        "System Diagnosis:\n"
    )

    print(
        f"Failure Stage: {failure_stage}"
    )

    print(
        f"Actual Failure Reason: {actual_failure_reason}"
    )

    print(
        "\n--------------------------------------\n"
    )

    reflection_output = run_reflection_llm(
        user_input=user_input,
        failure_stage=failure_stage,
        actual_failure_reason=actual_failure_reason,
        planner_output=planner_output,
        validation_output=validation_output,
        execution_result=execution_result
    )

    print(
        "\nStructured Reflection Output:\n"
    )

    print(reflection_output)

    print(
        "\n======================================\n"
    )

    return reflection_output