def generate_kpis(monthly):
    avg = monthly["revenue"].mean()

    
    best_row = monthly.loc[monthly["revenue"].idxmax()]
    worst_row = monthly.loc[monthly["revenue"].idxmin()]

    period_col = "month" if "month" in monthly.columns else "date"

    best = best_row[period_col]
    worst = worst_row[period_col]

    volatility = monthly["revenue"].std()

    return {
        "avg_monthly_revenue": round(avg, 2),
        "best_month": str(best),
        "worst_month": str(worst),
        "revenue_volatility": round(volatility, 2)
    }
