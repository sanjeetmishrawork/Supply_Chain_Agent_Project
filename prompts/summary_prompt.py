# SUMMARY_PROMPT = """
# You are writing for senior executives.

# Summarize the following operational case:

# Item ID: {item_id}
# Store ID: {store_id}

# Root Cause: {root_cause}
# Recommended Action: {recommended_action}
# Business Impact: {business_impact}

# Return a concise executive summary in 4–5 lines.

# It should sound boardroom-ready.
# Clear.
# Decisive.
# Strategic.
# """

SUMMARY_PROMPT = """
You are writing for senior executives.

Summarize the following operational case.

Product Information:
Item ID: {item_id}
Store ID: {store_id}
Category: {category}

Diagnosis:
Root Cause: {root_cause}

Recommendation:
Recommended Action: {recommended_action}

Business Impact:
{business_impact}

Aggregated Business Context:
Total Items: {total_items}
High Risk Count: {high_risk_count}
Top Store: {top_store}

Return a concise executive summary in 4–5 lines.

It should be:
Clear
Decisive
Boardroom-ready
Strategic

Avoid technical noise.
"""