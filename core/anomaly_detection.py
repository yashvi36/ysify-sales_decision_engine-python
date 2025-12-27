import pandas as pd
import numpy as np

def detect_anomalies(monthly_df):
    df = monthly_df.copy()

    mean_revenue = df["revenue"].mean()
    std_revenue = df["revenue"].std()

    df["z_score"] = (df["revenue"] - mean_revenue) / std_revenue

    anomalies = []

    for _, row in df.iterrows():
        if abs(row["z_score"]) > 2:
            anomaly_type = (
                "Unusual Spike" if row["z_score"] > 0 else "Unusual Drop"
            )

            anomalies.append({
                "month": row["date"],
                "revenue": round(row["revenue"], 2),
                "type": anomaly_type,
                "z_score": round(row["z_score"], 2)
            })

    return anomalies
