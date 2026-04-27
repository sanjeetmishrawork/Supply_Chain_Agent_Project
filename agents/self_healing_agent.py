# agents/self_healing_agent.py

import json

from llm.repair_llm import run_repair_llm


def auto_repair_query_plan(
    user_input,
    query_plan,
    validation_result
):
    """
    Self-Healing Agent

    Purpose:
    Apply minimal safe repair
    using validator-guided LLM patching.

    Flow:

    Invalid Query Plan
    ↓
    Repair Prompt
    ↓
    Repair LLM returns JSON patch
    ↓
    Safe merge into original plan
    ↓
    Validator retry

    IMPORTANT:

    This is NOT re-planning.

    This is:
    surgical correction only.

    We merge patches.

    We do NOT replace
    the full query plan.

    Retry policy:
    exactly one retry.
    """

    print(
        "\n========== SELF-HEALING AGENT ==========\n"
    )

    print(
        "Original Failed Query Plan:\n"
    )
    print(query_plan)

    print(
        "\nValidation Failure:\n"
    )
    print(validation_result)

    # -----------------------------------
    # Step 1
    # Call Repair LLM
    # -----------------------------------

    raw_patch = run_repair_llm(
        user_input=user_input,
        query_plan=query_plan,
        validation_result=validation_result
    )

    # -----------------------------------
    # Step 2
    # Parse JSON Patch
    # -----------------------------------

    try:
        repair_patch = json.loads(
            raw_patch
        )

    except Exception:
        print(
            "\nRepair failed: invalid JSON patch returned.\n"
        )

        print(
            "Skipping auto-repair.\n"
        )

        print(
            "========================================\n"
        )

        return query_plan

    if not isinstance(
        repair_patch,
        dict
    ):
        print(
            "\nRepair failed: patch is not a dictionary.\n"
        )

        print(
            "Skipping auto-repair.\n"
        )

        print(
            "========================================\n"
        )

        return query_plan

    print(
        "\nParsed Repair Patch:\n"
    )
    print(repair_patch)

    # -----------------------------------
    # Step 3
    # Safe Merge
    # -----------------------------------

    repaired_query_plan = (
        query_plan.copy()
    )

    repaired_query_plan.update(
        repair_patch
    )

    print(
        "\nFinal Repaired Query Plan:\n"
    )
    print(repaired_query_plan)

    print(
        "\n========================================\n"
    )

    return repaired_query_plan