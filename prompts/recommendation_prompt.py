# RECOMMENDATION_PROMPT = """
# You are a senior retail supply chain decision expert.

# Analyze the following case:

# Item ID: {item_id}
# Store ID: {store_id}

# Root Cause: {root_cause}
# Inventory Risk: {inventory_risk}
# Price Sensitivity: {price_sensitivity}
# Anomaly Score: {anomaly_score}

# Choose the SINGLE best operational action from:

# 1. Increase safety stock
# 2. Reduce aggressive promotions
# 3. Improve replenishment frequency
# 4. Review pricing strategy
# 5. Escalate supplier coordination

# Return exactly in this format:

# Recommended Action: <best action>
# Priority Level: <HIGH / MEDIUM / LOW>
# Reason: <one concise business sentence>

# Do not provide multiple actions.
# Be specific and practical.
# """

RECOMMENDATION_PROMPT = """
You are a senior retail supply chain decision expert.

Analyze the following operational context.

Product Information:
Item ID: {item_id}
Store ID: {store_id}
Category: {category}

Diagnosis:
Root Cause: {root_cause}

Inventory Signals:
Inventory Risk: {inventory_risk}
Price Sensitivity: {price_sensitivity}
Anomaly Score: {anomaly_score}

Aggregated Business Context:
Total Items: {total_items}
High Risk Count: {high_risk_count}
Top Store: {top_store}

Your task:

If this is a product query:
→ recommend the best operational corrective action

If this is a category/store query:
→ recommend the best strategic intervention

Choose ONLY ONE strongest action from:

1. Increase safety stock
2. Reduce aggressive promotions
3. Improve replenishment frequency
4. Review pricing strategy
5. Escalate supplier coordination

Return exactly in this format:

Recommended Action: <best action>
Priority Level: <HIGH / MEDIUM / LOW>
Reason: <one concise business sentence>

Do not provide multiple actions.
Be practical and decisive.
"""