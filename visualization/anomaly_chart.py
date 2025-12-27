import matplotlib.pyplot as plt
import os

def anomaly_chart(monthly_df, anomalies):
    os.makedirs("output/charts", exist_ok=True)

    months = monthly_df["date"]
    revenue = monthly_df["revenue"]

    plt.figure(figsize=(8, 4))
    plt.plot(months, revenue, marker="o", label="Revenue")

    # Highlight anomalies
    for anomaly in anomalies:
        idx = monthly_df[monthly_df["date"] == anomaly["month"]].index
        if not idx.empty:
            plt.scatter(
                months.loc[idx],
                revenue.loc[idx],
                color="red",
                s=100,
                label="Anomaly"
            )

    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Monthly Sales with Anomaly Detection")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig("output/charts/anomalies.png")
    plt.close()
