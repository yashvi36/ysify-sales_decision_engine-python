import matplotlib.pyplot as plt
import os

def revenue_pie_chart(df, mode="category"):
    os.makedirs("output/charts", exist_ok=True)

    if mode == "category":
        data = df.groupby("category")["revenue"].sum()
        title = "Revenue Distribution by Category"
        file_name = "revenue_pie_category.png"
    else:
        data = df.groupby("region")["revenue"].sum()
        title = "Revenue Distribution by Region"
        file_name = "revenue_pie_region.png"

    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            value = int(round(pct * total / 100.0))
            return f"{pct:.1f}%\n₹{value:,}"
        return my_format

    plt.figure(figsize=(6, 6))
    plt.pie(
        data,
        labels=data.index,
        autopct=autopct_format(data),
        startangle=140,
        wedgeprops={"edgecolor": "white"},
        textprops={"fontsize": 9}
    )

    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"output/charts/{file_name}")
    plt.close()

    return file_name
