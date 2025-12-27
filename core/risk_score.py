import numpy as np

def calculate_risk(monthly_df, forecast):
    growth = monthly_df["growth_pct"].dropna()
    volatility = np.std(growth)

    last_growth = growth.iloc[-1]
    avg_forecast = sum(f["predicted_revenue"] for f in forecast) / len(forecast)

    score = 0

    if last_growth < 0:
        score += 40

    if volatility > 15:
        score += 30

    if avg_forecast < monthly_df["revenue"].mean():
        score += 30

    level = (
        "High Risk" if score >= 60 else
        "Medium Risk" if score >= 30 else
        "Low Risk"
    )

    return {
        "risk_score": score,
        "risk_level": level
    }
