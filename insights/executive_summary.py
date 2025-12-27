def generate_summary(decision, top_category, risk, forecast):
    business_health = decision.get("business_health", "Unknown")
    action = decision.get("action", "No action defined")

    risk_level = risk.get("risk_level", "unknown risk")

    commentary = (
        f"The business is currently showing a {business_health.lower()} trend. "
        f"The top performing category is {top_category}. "
        f"Overall risk level is {risk_level}, "
        f"with stable forecast expected over the next quarter."
    )

    return {
        "business_health": business_health,
        "top_category": top_category,
        "action": action,
        "executive_commentary": commentary
    }
