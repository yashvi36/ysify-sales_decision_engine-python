import matplotlib.pyplot as plt
import os

def forecast_chart(forecast_data):
    os.makedirs("output/charts", exist_ok=True)

    months = [f["month"] for f in forecast_data]
    values = [f["predicted_revenue"] for f in forecast_data]
    lower = [f["lower_bound"] for f in forecast_data]
    upper = [f["upper_bound"] for f in forecast_data]

    plt.figure(figsize=(8, 4))

    # Main forecast line
    plt.plot(months, values, marker="o", linewidth=2, label="Forecast", color="#1f77b4")

    # Confidence band
    plt.fill_between(
        months,
        lower,
        upper,
        color="#1f77b4",
        alpha=0.2,
        label="Confidence Range"
    )

    # ---------------- ANNOTATIONS (STOCK STYLE) ----------------
    for i in range(1, len(values)):
        prev = values[i - 1]
        curr = values[i]
        pct_change = ((curr - prev) / prev) * 100

        if pct_change >= 0:
            arrow = "↑"
            color = "green"
            text = f"+{pct_change:.1f}%"
        else:
            arrow = "↓"
            color = "red"
            text = f"{pct_change:.1f}%"

        plt.annotate(
            f"{arrow} {text}",
            xy=(months[i], curr),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            color=color,
            fontsize=9,
            fontweight="bold"
        )

    # ---------------- OVERALL TREND LABEL ----------------
    overall_change = ((values[-1] - values[0]) / values[0]) * 100

    if overall_change > 2:
        signal = "📈 Bullish Trend"
        signal_color = "green"
    elif overall_change < -2:
        signal = "📉 Bearish Trend"
        signal_color = "red"
    else:
        signal = "➖ Sideways Trend"
        signal_color = "gray"

    plt.text(
        0.01, 0.95,
        signal,
        transform=plt.gca().transAxes,
        fontsize=11,
        fontweight="bold",
        color=signal_color,
        verticalalignment="top"
    )

    plt.title("3-Month Sales Forecast (Market-Style Projection)")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/charts/forecast.png")
    plt.close()