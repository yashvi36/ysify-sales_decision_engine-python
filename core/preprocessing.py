import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path)

    df['date'] = pd.to_datetime(df['date'])
    df['revenue'] = df['price'] * df['quantity']

    return df
