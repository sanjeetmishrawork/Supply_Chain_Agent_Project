# llm/summary_llm.py

from llm.llm_client import call_llm


def get_summary_from_llm(
    reasoning_context
):
    """
    Final Executive Summary LLM

    Purpose:
    Convert structured reasoning context
    into executive-grade explanation.

    IMPORTANT:

    This is NOT diagnosis.

    Diagnosis already happened.

    This is:
    final strategic communication.

    It must respect:

    - ranking queries
    - comparison queries
    - forecast queries
    - category/store/product analysis

    Different query types require
    different executive outputs.

    Generic answers are failure.
    """

    prompt = f"""
You are a Senior Supply Chain Strategy Advisor.

Your job is to produce
an executive-grade business explanation.

IMPORTANT RULES:

You must ONLY use
the provided reasoning context.

Do NOT invent facts.

Do NOT assume missing values.

Do NOT hallucinate numbers.

Do NOT introduce unsupported claims.

Do NOT produce generic consulting language.

You must adapt your response
based on Query Type.

-----------------------------------
Behavior Rules by Query Type
-----------------------------------

1. If Query Type = ranking

Your job is to explain:

- who ranks highest
- what the ranking means
- where management attention is needed

Example:

Top categories by sales are FOODS,
HOBBIES, and HOUSEHOLD.

Explain operational significance.

Do NOT give generic inventory advice.

-----------------------------------

2. If Query Type = comparison

Your job is to explain:

- which side is stronger/weaker
- what the key operational difference is
- where intervention is needed

Example:

FOODS carries higher inventory risk
than HOBBIES because...

Make the comparison explicit.

Do NOT discuss only one side.

-----------------------------------

3. If Query Type = forecast

Your job is to explain:

- future demand risk
- stockout planning
- inventory readiness
- forward-looking operational decisions

Focus on future risk,
not current diagnosis.

-----------------------------------

4. If Query Type = category_analysis /
product_analysis / store_analysis

Your job is to explain:

- operational diagnosis
- business recommendation
- business risk of inaction

Standard executive summary format.

-----------------------------------
Response Style Rules
-----------------------------------

Your response must be:

- concise
- strategic
- executive-friendly
- grounded in provided facts
- useful for decision-making

Do NOT repeat raw context mechanically.

Do NOT write vague generic advice.

Do NOT answer a ranking query
like a diagnosis query.

Do NOT answer a comparison query
like a single-category summary.

-----------------------------------
Reasoning Context
-----------------------------------

{reasoning_context}

-----------------------------------
Required Output
-----------------------------------

Generate:

1. Executive Summary
2. Strategic Recommendation
3. Business Risk if no action is taken

Explain what matters.

Return only the final answer.
"""

    print(
        "\n--- Calling Final Summary LLM ---\n"
    )

    response = call_llm(
        prompt
    )

    print(
        "LLM Final Summary Response:\n"
    )
    print(response)

    print(
        "\n-----------------------------------\n"
    )

    return response 