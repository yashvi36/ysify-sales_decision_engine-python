# ===================== IMPORTS =====================
import streamlit as st
import pandas as pd
import json
import os

from core.preprocessing import load_and_clean_data
from core.time_series import monthly_sales
from core.growth_driver import category_performance
from core.decision_engine import business_decision
from core.forecast import forecast_next_months
from core.risk_score import calculate_risk
from core.kpi import generate_kpis
from core.anomaly_detection import detect_anomalies

from visualization.charts import sales_trend_chart
from visualization.forecast_chart import forecast_chart
from visualization.anomaly_chart import anomaly_chart
from visualization.pie_chart import revenue_pie_chart
from insights.executive_summary import generate_summary


# ===================== PAGE CONFIG (FIRST STREAMLIT CALL) =====================
st.set_page_config(
    page_title="Sales Decision Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===================== GLOBAL UI THEME =====================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    font-weight: 600;
}
.metric-card {
    background-color: #161b22;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 0 0 1px #30363d;
}
.section-divider {
    margin: 40px 0;
    border-top: 1px solid #30363d;
}
img {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ===================== HEADER =====================
st.title("📊 Sales Decision Intelligence Dashboard")
st.write("Upload your sales file (CSV / Excel / TXT) to generate insights")


# ===================== FILE UPLOAD =====================
uploaded_file = st.file_uploader(
    "Upload file",
    type=["csv", "xlsx", "txt"]
)

if uploaded_file:
    # ---------- Read file ----------
    if uploaded_file.name.endswith((".csv", ".txt")):
        base_df = pd.read_csv(uploaded_file)
    else:
        base_df = pd.read_excel(uploaded_file)

    # ---------- Validation ----------
    required_cols = {"date", "product", "category", "region", "price", "quantity"}
    if not required_cols.issubset(base_df.columns):
        st.error("❌ Invalid file format. Required columns: date, product, category, region, price, quantity")
        st.stop()

    st.success("File uploaded successfully")

    # ===================== SIDEBAR FILTERS =====================
    st.sidebar.header("🔍 Filters")

    selected_category = st.sidebar.multiselect(
        "Category",
        options=base_df["category"].unique(),
        default=list(base_df["category"].unique())
    )

    selected_region = st.sidebar.multiselect(
        "Region",
        options=base_df["region"].unique(),
        default=list(base_df["region"].unique())
    )

    df = base_df[
        base_df["category"].isin(selected_category) &
        base_df["region"].isin(selected_region)
    ]

    if df.empty:
        st.warning("⚠️ No data available for selected filters.")
        st.stop()

    # ===================== EDITABLE TABLE =====================
    st.markdown("## 📝 Edit Data (Optional)")
    st.caption("Edit values below and click **Save Changes** to apply updates.")

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
    )

    save_changes = st.button("💾 Save Changes")

    # ---------- APPLY EDITED DATA ----------
    if save_changes:
        df = edited_df.copy()
        st.success("✅ Changes saved and applied")
    else:
        df = edited_df.copy()

    # ---------- Safety validation after edit ----------
    if (df["price"] <= 0).any() or (df["quantity"] <= 0).any():
        st.error("❌ Price and Quantity must be positive values")
        st.stop()

    # ===================== ENGINE PIPELINE =====================
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/temp_sales.csv", index=False)

    df = load_and_clean_data("data/temp_sales.csv")
    monthly = monthly_sales(df)
    category_df = category_performance(df)

    decision = business_decision(monthly)
    forecast = forecast_next_months(monthly)
    risk = calculate_risk(monthly, forecast)
    anomalies = detect_anomalies(monthly)

    summary = generate_summary(
        decision,
        category_df.iloc[0]["category"],
        risk,
        forecast
    )

    summary["kpis"] = generate_kpis(monthly)
    summary["anomalies"] = anomalies

    # ===================== KPI CARDS =====================
    st.markdown("## 📌 Key Metrics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Monthly Revenue", f"₹{summary['kpis']['avg_monthly_revenue']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Best Month", summary["kpis"]["best_month"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Worst Month", summary["kpis"]["worst_month"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        if len(monthly) >= 2:
            last = monthly.iloc[-1]["revenue"]
            prev = monthly.iloc[-2]["revenue"]
            mom_growth = ((last - prev) / prev) * 100
            value = f"{mom_growth:.2f}%"
        else:
            value = "N/A"

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("MoM Growth", value)
        st.markdown('</div>', unsafe_allow_html=True)

    # ===================== EXECUTIVE INSIGHT =====================
    st.markdown("## 🧠 Executive Insight")
    st.markdown(
        f"""
        <div class="metric-card">
            {summary["executive_commentary"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ===================== BUSINESS HEALTH =====================
    risk_level = risk["risk_level"].lower()
    if "low" in risk_level:
        st.success("🟢 Business Health: Stable")
    elif "medium" in risk_level:
        st.warning("🟡 Business Health: Monitor Closely")
    else:
        st.error("🔴 Business Health: High Risk")

    # ===================== SMART RECOMMENDATIONS =====================
    st.markdown("## 🤖 Smart Recommendations")

    if "electronics" in summary["top_category"].lower():
        st.write("• Increase inventory and promotions for Electronics")

    if "upward" in summary["business_health"].lower():
        st.write("• Consider expanding sales channels")

    if anomalies:
        st.write("• Investigate detected sales anomalies")

    # ===================== CHARTS =====================
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 Sales Analytics")

    left, right = st.columns(2)

    with left:
        st.markdown("### 📈 Sales Trend")
        sales_trend_chart(monthly)
        st.image("output/charts/sales_trend.png", width=520)

    with right:
        st.markdown("### 🔮 Forecast")
        forecast_chart(forecast)
        st.image("output/charts/forecast.png", width=520)

    st.markdown("### 🚨 Anomaly Detection")
    anomaly_chart(monthly, anomalies)
    st.image("output/charts/anomalies.png", width=520)

    # ===================== PIE CHART WITH TOGGLE =====================
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🥧 Revenue Distribution")

    pie_mode = st.radio(
        "View distribution by:",
        ["Category", "Region"],
        horizontal=True
    )

    mode = "category" if pie_mode == "Category" else "region"
    pie_file = revenue_pie_chart(df, mode)

    st.image(f"output/charts/{pie_file}", width=520)

    # ===================== DOWNLOADS =====================
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Analysis Report (JSON)",
        json.dumps(summary, indent=4),
        file_name="sales_analysis_report.json",
        mime="application/json"
    )

    if st.button("📥 Generate Excel Report"):
        os.makedirs("output", exist_ok=True)
        excel_path = "output/sales_report.xlsx"

        with pd.ExcelWriter(excel_path) as writer:
            monthly.to_excel(writer, sheet_name="Monthly Sales", index=False)
            pd.DataFrame(anomalies).to_excel(writer, sheet_name="Anomalies", index=False)

        with open(excel_path, "rb") as f:
            st.download_button(
                "⬇️ Download Excel Report",
                f,
                file_name="sales_report.xlsx"
            )

    # ===================== RAW JSON =====================
    with st.expander("📄 View Full Analysis (JSON)"):
        st.json(summary)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.caption("Sales Decision Intelligence Engine • Internal Analytics Tool • v1.0")
