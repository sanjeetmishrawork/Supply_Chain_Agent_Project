
# agents/validation_agent.py

import json
import re

from llm.validator_llm import run_validator_llm


# =====================================
# DETERMINISTIC GUARDRAILS
# =====================================

ALLOWED_INTENTS = [
    "product_diagnosis",
    "category_analysis",
    "department_analysis",
    "store_analysis",
    "state_analysis",
    "recommendation_request",
    "business_impact",
    "forecasting_query",
    "ranking_query",
    "comparison_query",
    "trend_query",
    "executive_summary",
    "discovery_query",
    "root_cause_query",
    "exception_query",
    "threshold_query",
    "portfolio_summary",
    "intervention_priority",
    "price_sensitivity_query"
]

ALLOWED_ENTITY_TYPES = [
    "item_id",
    "category",
    "department",
    "store_id",
    "state_id",
    "field",
    "none"
]

ALLOWED_METRICS = [
    "sales",
    "inventory_risk",
    "stockout_risk",
    "anomaly_score",
    "price_sensitivity",
    "forecast_next_7_days",
    "forecast_next_30_days",
    "avg_daily_sales",
    "zero_sales_days",
    "sales_volatility"
]


def extract_json_block(text):
    """
    Extract JSON safely from LLM output.

    Because LLMs love decoration.
    We prefer JSON.
    """

    try:
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if match:
            return match.group()

        return None

    except Exception:
        return None


def deterministic_validate(query_plan):
    """
    Deterministic validation first.

    Cheap.
    Reliable.
    No token billing.

    Python handles structure.

    LLM handles judgment.

    Never reverse that.
    """

    issues = []

    intent = query_plan.get(
        "intent",
        ""
    )

    entity_type = query_plan.get(
        "entity_type",
        ""
    )

    entity_value = query_plan.get(
        "entity_value",
        ""
    )

    metric = query_plan.get(
        "metric",
        ""
    )

    aggregation = query_plan.get(
        "aggregation",
        ""
    )

    limit = query_plan.get(
        "limit",
        None
    )

    comparison_target = query_plan.get(
        "comparison_target",
        ""
    )

    operation = query_plan.get(
        "operation",
        ""
    )

    target_field = query_plan.get(
        "target_field",
        ""
    )

    threshold = query_plan.get(
        "threshold",
        None
    )

    # =====================================
    # ALLOWED VALUES
    # =====================================

    if intent not in ALLOWED_INTENTS:
        issues.append(
            "Invalid intent"
        )

    if entity_type not in ALLOWED_ENTITY_TYPES:
        issues.append(
            "Invalid entity type"
        )

    if metric and metric not in ALLOWED_METRICS:
        issues.append(
            "Metric is not allowed"
        )

    # =====================================
    # REQUIRED ENTITY VALIDATION
    # =====================================

    if intent in [
        "product_diagnosis",
        "category_analysis",
        "department_analysis",
        "store_analysis",
        "state_analysis",
        "comparison_query",
        "root_cause_query"
    ]:
        if (
            entity_type != "none"
            and not entity_value
        ):
            issues.append(
                "Missing required entity_value"
            )

    # =====================================
    # ITEM_ID FORMAT VALIDATION
    # =====================================

    if (
        entity_type == "item_id"
        and entity_value
    ):
        item_pattern = (
            r"^[A-Z]+_[0-9]+_[0-9]+$"
        )

        if not re.match(
            item_pattern,
            str(entity_value).upper()
        ):
            issues.append(
                "Invalid item_id format. "
                "Expected format like "
                "FOODS_1_005"
            )

    # =====================================
    # RANKING QUERY RULES
    # =====================================

    if intent == "ranking_query":

        if not aggregation:
            issues.append(
                "Ranking query requires aggregation"
            )

        if (
            limit is None
            or limit <= 0
        ):
            issues.append(
                "Ranking query requires limit > 0"
            )

        if not metric:
            issues.append(
                "Ranking query requires metric"
            )

    # =====================================
    # COMPARISON QUERY RULES
    # =====================================

    if intent == "comparison_query":

        if not comparison_target:
            issues.append(
                "Comparison query requires comparison_target"
            )

        if not metric:
            issues.append(
                "Comparison query requires metric"
            )

    # =====================================
    # FORECASTING QUERY RULES
    # =====================================

    if intent == "forecasting_query":

        if not metric:
            issues.append(
                "Forecasting query requires metric"
            )

    # =====================================
    # ROOT CAUSE QUERY RULES
    # =====================================

    if intent == "root_cause_query":

        if not metric:
            issues.append(
                "Root cause query requires metric"
            )

        if (
            entity_type != "none"
            and not entity_value
        ):
            issues.append(
                "Root cause query requires entity_value"
            )

    # =====================================
    # STATE ANALYSIS RULES
    # =====================================

    if intent == "state_analysis":

        if entity_type != "state_id":
            issues.append(
                "State analysis requires entity_type = state_id"
            )

        if not entity_value:
            issues.append(
                "State analysis requires entity_value"
            )

    # =====================================
    # THRESHOLD QUERY RULES
    # =====================================

    if intent == "threshold_query":

        if not metric:
            issues.append(
                "Threshold query requires metric"
            )

        if threshold is None:
            issues.append(
                "Threshold query requires threshold"
            )

    # =====================================
    # PRICE SENSITIVITY RULES
    # =====================================

    if intent == "price_sensitivity_query":

        if not metric:
            issues.append(
                "Price sensitivity query requires metric"
            )

    # =====================================
    # DISCOVERY QUERY RULES
    # =====================================

    if intent == "discovery_query":

        if not operation:
            issues.append(
                "Discovery query requires operation"
            )

        if not target_field:
            issues.append(
                "Discovery query requires target_field"
            )

        allowed_operations = [
            "distinct_values",
            "schema_lookup"
        ]

        if (
            operation
            and operation not in allowed_operations
        ):
            issues.append(
                "Invalid discovery operation"
            )

    # =====================================
    # FINAL DETERMINISTIC RESULT
    # =====================================

    if issues:
        return {
            "is_valid": False,
            "issues": issues,
            "suggested_fix": (
                "Fix deterministic validation issues first"
            )
        }

    return {
        "is_valid": True,
        "issues": [],
        "suggested_fix": ""
    }


def validate_query_plan(query_plan):
    """
    Hybrid Validation

    Step 1:
    deterministic validation

    Step 2:
    LLM semantic validation

    This is the execution gatekeeper.
    """

    print(
        "\n--- Deterministic Validation ---\n"
    )

    deterministic_result = (
        deterministic_validate(
            query_plan
        )
    )

    print(
        deterministic_result
    )

    # =====================================
    # HARD REJECT FIRST
    # =====================================

    if not deterministic_result.get(
        "is_valid",
        False
    ):
        print(
            "\nDeterministic validation failed.\n"
        )

        return deterministic_result

    # =====================================
    # THEN LLM VALIDATION
    # =====================================

    print(
        "\n--- Calling Validator LLM ---\n"
    )

    raw_response = run_validator_llm(
        query_plan
    )

    json_block = extract_json_block(
        raw_response
    )

    if not json_block:
        print(
            "\nValidator failed to produce JSON.\n"
        )

        return {
            "is_valid": False,
            "issues": [
                "Validator parsing failed"
            ],
            "suggested_fix": (
                "Fallback to safe route"
            )
        }

    try:
        parsed_validation = json.loads(
            json_block
        )

        print(
            "\nLLM Validation Result:\n"
        )
        print(parsed_validation)

        return parsed_validation

    except Exception as e:
        print(
            "\nValidator JSON parsing failed:",
            str(e)
        )

        return {
            "is_valid": False,
            "issues": [
                "Validator JSON parse failure"
            ],
            "suggested_fix": (
                "Fallback to safe route"
            )
        }
