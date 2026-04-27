# chat_interface.py

import pandas as pd
import glob

from query_executor import execute_query_plan
from query_dsl_builder import build_query_dsl

from agents.prompt_planner import plan_user_query
from agents.validation_agent import validate_query_plan
from agents.reasoning_agent import generate_business_reasoning
from agents.reflection_agent import reflect_on_failure
from agents.self_healing_agent import auto_repair_query_plan


def load_inventory_data():
    """
    Load gold inventory risk table
    """
    return pd.read_csv(
        "data/gold_inventory_risk.csv"
    )


def load_price_signal():
    """
    Load price impact signal
    """
    files = glob.glob(
        "data/gold_price_impact/*.csv"
    )

    if not files:
        return "MEDIUM"

    df = pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )

    if "price_sensitivity_flag" in df.columns:
        if (
            df["price_sensitivity_flag"] == "HIGH"
        ).sum() > 0:
            return "HIGH"

    return "MEDIUM"


def load_anomaly_signal():
    """
    Load anomaly severity signal
    """
    files = glob.glob(
        "data/gold_demand_anomaly/*.csv"
    )

    if not files:
        return ("MEDIUM", 5.0)

    df = pd.concat(
        [pd.read_csv(f) for f in files],
        ignore_index=True
    )

    if "anomaly_score" in df.columns:
        max_score = float(
            df["anomaly_score"].max()
        )

        if max_score > 5:
            return ("HIGH", max_score)

        return ("MEDIUM", max_score)

    return ("MEDIUM", 5.0)


def run_agent():
    """
    Strategic Copilot
    with visible reasoning
    """

    print(
        "\nSupply Chain Strategic Copilot Ready"
    )
    print(
        "This application helps analyze supply chain risk, validate query plans, execute structured queries, and generate business reasoning."
    )
    print(
        "Type your business question and press Enter."
    )
    print(
        "If you press Enter without typing anything, the application will ask the same question again."
    )
    print(
        "Type 'help' to see these instructions again."
    )
    print(
        "Type 'exit' or press Ctrl+C to close the application.\n"
    )

    inventory_df = load_inventory_data()

    if inventory_df.empty:
        print(
            "Inventory data not found."
        )
        return

    while True:

        user_input = input(
            "Ask your question: "
        ).strip()

        if not user_input:
            print(
                "\nNo input detected. Please enter your question. Type 'help' for guidance.\n"
            )
            continue

        if user_input.lower() == "help":
            print(
                "\nThis application helps analyze supply chain risk, validate query plans, execute structured queries, and generate business reasoning."
            )
            print(
                "Ask a business question related to supply chain decisions."
            )
            print(
                "Type 'exit' or press Ctrl+C to close the application.\n"
            )
            continue

        if user_input.lower() == "exit":
            print(
                "Exiting Strategic Copilot."
            )
            break

        # =====================================
        # STEP 1: PROMPT PLANNING
        # =====================================

        print(
            "\n===================================="
        )
        print(
            "STEP 1: PROMPT PLANNING"
        )
        print(
            "====================================\n"
        )

        planner_result = plan_user_query(
            user_input
        )

        reasoning_steps = planner_result.get(
            "reasoning_steps",
            []
        )

        query_plan = planner_result.get(
            "query_plan",
            {}
        )

        print(
            "\nPlanner Reasoning Steps:\n"
        )

        for step in reasoning_steps:
            print(step)

        print(
            "\nStructured Query Plan:\n"
        )
        print(query_plan)

        # =====================================
        # STEP 2: VALIDATION
        # =====================================

        print(
            "\n===================================="
        )
        print(
            "STEP 2: VALIDATION"
        )
        print(
            "====================================\n"
        )

        validation_result = validate_query_plan(
            query_plan
        )

        print(
            "\nValidation Result:\n"
        )
        print(validation_result)

        # -----------------------------------
        # VALIDATION FAILURE
        # SELF-HEALING FIRST
        # -----------------------------------

        if not validation_result.get(
            "is_valid",
            False
        ):
            print(
                "\nInitial validation failed.\n"
            )

            print(
                "\n===================================="
            )
            print(
                "STEP 2A: AUTO-REPAIR ATTEMPT"
            )
            print(
                "====================================\n"
            )

            repaired_query_plan = (
                auto_repair_query_plan(
                    user_input=user_input,
                    query_plan=query_plan,
                    validation_result=validation_result
                )
            )

            print(
                "\n===================================="
            )
            print(
                "STEP 2B: VALIDATION RETRY"
            )
            print(
                "====================================\n"
            )

            retry_validation_result = (
                validate_query_plan(
                    repaired_query_plan
                )
            )

            print(
                "\nRetry Validation Result:\n"
            )
            print(
                retry_validation_result
            )

            # -----------------------------------
            # RETRY SUCCESS
            # -----------------------------------

            if retry_validation_result.get(
                "is_valid",
                False
            ):
                print(
                    "\nAuto-repair successful. Continuing execution.\n"
                )

                query_plan = repaired_query_plan
                validation_result = (
                    retry_validation_result
                )

            # -----------------------------------
            # RETRY FAILURE
            # REFLECTION + STOP
            # -----------------------------------

            else:
                print(
                    "\nAuto-repair failed.\n"
                )

                reflect_on_failure(
                    user_input=user_input,

                    failure_stage="validation",

                    actual_failure_reason=(
                        retry_validation_result.get(
                            "issues",
                            [
                                "Validation failed after auto-repair"
                            ]
                        )
                    ),

                    planner_output=repaired_query_plan,

                    validation_output=(
                        retry_validation_result
                    ),

                    execution_result=(
                        "Validation failed even after auto-repair"
                    )
                )

                continue

        # =====================================
        # STEP 3: QUERY EXECUTION
        # =====================================

        print(
            "\n===================================="
        )
        print(
            "STEP 3: QUERY EXECUTION"
        )
        print(
            "====================================\n"
        )

        # -----------------------------------
        # STEP 3A
        # Build Query DSL
        # -----------------------------------

        dsl = build_query_dsl(
            query_plan
        )

        print(
            "\nGenerated Query DSL:\n"
        )
        print(dsl)

        # -----------------------------------
        # STEP 3B
        # Execute Query DSL
        # -----------------------------------

        query_context = execute_query_plan(
            inventory_df,
            dsl
        )

        print(
            "\nExecution Context:\n"
        )
        print(query_context)

        # -----------------------------------
        # EMPTY QUERY RESULT
        # -----------------------------------

        if not query_context:
            print(
                "\nNo query results found.\n"
            )

            reflect_on_failure(
                user_input=user_input,

                failure_stage="execution",

                actual_failure_reason=(
                    "Query execution returned no matching "
                    "records for the generated DSL query"
                ),

                planner_output=query_plan,

                validation_output=validation_result,

                execution_result=(
                    "Empty query result"
                )
            )

            continue

        # =====================================
        # STEP 4: BUSINESS REASONING
        # =====================================

        print(
            "\n===================================="
        )
        print(
            "STEP 4: BUSINESS REASONING"
        )
        print(
            "====================================\n"
        )

        final_response = (
            generate_business_reasoning(
                query_plan=query_plan,
                query_context=query_context
            )
        )

        print(
            "\n========== FINAL ANSWER ==========\n"
        )
        print(final_response)

        print(
            "\n==================================\n"
        )


if __name__ == "__main__":
    run_agent()