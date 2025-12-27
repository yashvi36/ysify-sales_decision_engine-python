def monthly_sales(df):
    monthly = (
        df
        .groupby(df['date'].dt.to_period('M'))['revenue']
        .sum()
        .reset_index()
    )

    monthly['date'] = monthly['date'].astype(str)
    monthly['growth_pct'] = monthly['revenue'].pct_change() * 100
    monthly['moving_avg'] = monthly['revenue'].rolling(3).mean()

    return monthly
