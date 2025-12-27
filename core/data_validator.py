def validate_sales_data(df):
    required = {"date", "product", "category", "region", "price", "quantity"}

    if not required.issubset(df.columns):
        return False, "Missing required columns"

    if df.isnull().any().any():
        return False, "Null values detected"

    if (df["price"] <= 0).any() or (df["quantity"] <= 0).any():
        return False, "Invalid price or quantity"

    return True, "Valid"
