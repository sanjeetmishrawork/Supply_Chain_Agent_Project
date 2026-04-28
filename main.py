# main.py

from run_pipeline import execute_query


def main():
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

            final_state = execute_query(
                user_input
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

            if final_state.get(
                "failure_stage"
            ):
                print("System Reflection:\n")
                print(
                    final_state.get(
                        "reflection_output",
                        "No reflection available."
                    )
                )
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