
# main.py

from graph import build_graph


def main():
    """
    Clean runtime entry point

    Runs the full production pipeline:

    planner
    → validator
    → repair (if needed)
    → DSL
    → execution
    → reasoning
    → summary
    → reflection (on failure)
    """

    print("\n====================================")
    print("AI Supply Chain Strategic Copilot")
    print("====================================\n")

    while True:
        try:
            user_input = input(
                "Ask your question: "
            ).strip()

            if not user_input:
                print(
                    "\nPlease enter a valid question.\n"
                )
                continue

            if user_input.lower() in [
                "exit",
                "quit"
            ]:
                print(
                    "\nExiting Strategic Copilot.\n"
                )
                break

            # -----------------------------------
            # Initial LangGraph State
            # -----------------------------------

            initial_state = {
                "user_input": user_input,

                "query_plan": {},
                "planner_reasoning": "",

                "validation_result": {},
                "repaired_query_plan": {},

                "dsl": {},
                "execution_result": {},

                "reasoning_context": "",
                "final_response": "",

                "failure_stage": "",
                "actual_failure_reason": "",
                "reflection_output": "",

                "confidence_score": 0.0
            }

            # -----------------------------------
            # Build + Run Graph
            # -----------------------------------

            app = build_graph()

            final_state = app.invoke(
                initial_state
            )

            print(
                "\n===================================="
            )
            print(
                "FINAL EXECUTIVE OUTPUT"
            )
            print(
                "====================================\n"
            )

            # -----------------------------------
            # Failure Path
            # -----------------------------------

            if final_state.get(
                "failure_stage"
            ):
                print(
                    "System Reflection:\n"
                )

                print(
                    final_state.get(
                        "reflection_output",
                        "No reflection available."
                    )
                )

            # -----------------------------------
            # Success Path
            # -----------------------------------

            else:
                print(
                    final_state.get(
                        "final_response",
                        "No final response generated."
                    )
                )

            print(
                "\n====================================\n"
            )

        except KeyboardInterrupt:
            print(
                "\n\nExiting Strategic Copilot.\n"
            )
            break

        except Exception as e:
            print(
                f"\nSystem Error: {str(e)}\n"
            )


if __name__ == "__main__":
    main()
