# run_pipeline.py

from graph import build_graph


def execute_query(user_input):
    """
    Shared execution layer

    Used by:
    - CLI main.py
    - Streamlit frontend
    - Future API endpoints
    """

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

    app = build_graph()

    final_state = app.invoke(initial_state)

    return final_state