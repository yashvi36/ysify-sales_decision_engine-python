import json

from core.preprocessing import load_and_clean_data
from core.time_series import monthly_sales
from core.growth_driver import category_performance
from core.decision_engine import business_decision
from insights.executive_summary import generate_summary
from visualization.charts import sales_trend_chart
from core.forecast import forecast_next_months
from visualization.forecast_chart import forecast_chart
from core.risk_score import calculate_risk
from core.kpi import generate_kpis
from core.anomaly_detection import detect_anomalies
from visualization.anomaly_chart import anomaly_chart


def run_engine():
    # 1️⃣ Load & preprocess
    df = load_and_clean_data("data/sales.csv")

    # 2️⃣ Analysis
    monthly = monthly_sales(df)
    category_df = category_performance(df)

    # 3️⃣ Decision
    decision = business_decision(monthly)

    # 4️⃣ Forecast
    forecast = forecast_next_months(monthly)
    forecast_chart(forecast)

    # 5️⃣ Risk calculation
    risk = calculate_risk(monthly, forecast)

    # 6️⃣ Anomaly detection
    anomalies = detect_anomalies(monthly)
    
    anomaly_chart(monthly, anomalies)


    # 7️⃣ Summary (NOW all inputs exist)
    summary = generate_summary(
        decision,
        category_df.iloc[0]["category"],
        risk,
        forecast,

    )

    # 8️⃣ Add extra insights
    summary["kpis"] = generate_kpis(monthly)
    summary["anomalies"] = anomalies

    # 9️⃣ Save output
    with open("output/insights.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("✅ Sales Decision Engine executed successfully")


if __name__ == "__main__":
    run_engine()
