# STRATEGY_PROMPT = """
# You are a senior business strategy leader.

# Analyze this operational issue:

# Item ID: {item_id}
# Store ID: {store_id}

# Root Cause: {root_cause}
# Recommended Action: {recommended_action}
# Anomaly Score: {anomaly_score}

# Estimate the likely business impact.

# Return exactly in this format:

# Business Impact: <main impact>
# Urgency: <HIGH / MEDIUM / LOW>
# Estimated Financial Exposure: <realistic estimate>

# Be realistic.
# Avoid exaggerated financial numbers.
# Use executive language.
# """

STRATEGY_PROMPT = """
You are a senior business strategy leader.

Analyze this operational issue.

Product Information:
Item ID: {item_id}
Store ID: {store_id}
Category: {category}

Diagnosis:
Root Cause: {root_cause}

Recommendation:
Recommended Action: {recommended_action}

Aggregated Business Context:
Total Items: {total_items}
High Risk Count: {high_risk_count}
Top Store: {top_store}

Anomaly Score: {anomaly_score}

Estimate the likely business impact.

Return exactly in this format:

Business Impact: <main impact>
Urgency: <HIGH / MEDIUM / LOW>
Estimated Financial Exposure: <realistic estimate>

Be realistic.
Avoid exaggerated financial fantasy.
Use executive language.
"""