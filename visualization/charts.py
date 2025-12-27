import matplotlib.pyplot as plt
import os

def sales_trend_chart(monthly_df):
    os.makedirs("output/charts", exist_ok=True)
    

    plt.figure(figsize=(8, 4))
    plt.plot(monthly_df["date"], monthly_df["revenue"], marker="o", label="Revenue")
    plt.plot(monthly_df["date"], monthly_df["moving_avg"], linestyle="--", label="Moving Avg")

    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Monthly Sales Trend")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("output/charts/sales_trend.png")
    plt.close()
