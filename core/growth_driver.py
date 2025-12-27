def category_performance(df):
    return (
        df
        .groupby('category')['revenue']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
