import numpy as np
import pandas as pd

def forecast_next_months(monthly_df, months=3):
    last_revenue = monthly_df.iloc[-1]["revenue"]

    # Calculate historical volatility
    volatility = monthly_df["revenue"].pct_change().std()
    volatility = 0.05 if pd.isna(volatility) else volatility  # safety

    last_date = pd.Period(monthly_df.iloc[-1]["date"], freq="M")

    forecast = []
    current = last_revenue

    for i in range(1, months + 1):
        # Random up/down movement (stock-style)
        change_pct = np.random.normal(0, volatility)
        current = current * (1 + change_pct)

        forecast.append({
            "month": str(last_date + i),
            "predicted_revenue": round(current, 2),
            "lower_bound": round(current * 0.90, 2),
            "upper_bound": round(current * 1.10, 2)
        })

    return forecast
