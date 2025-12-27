import matplotlib.pyplot as plt
import os

def category_pie_chart(df):
    os.makedirs("output/charts", exist_ok=True)

    data = df.groupby("category")["revenue"].sum()

    plt.figure(figsize=(5, 5))
    plt.pie(data, labels=data.index, autopct="%1.1f%%", startangle=140)
    plt.title("Revenue Contribution by Category")
    plt.tight_layout()
    plt.savefig("output/charts/category_pie.png")
    plt.close()
