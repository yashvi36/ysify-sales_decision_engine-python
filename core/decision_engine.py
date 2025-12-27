def business_decision(monthly):
    trend = monthly["revenue"].diff().mean()

    if trend > 0:
        return {
            "business_health": "Upward",
            "action": "Scale operations and marketing"
        }
    elif trend < 0:
        return {
            "business_health": "Downward",
            "action": "Reduce costs and investigate decline"
        }
    else:
        return {
            "business_health": "Stable",
            "action": "Maintain current strategy"
        }
