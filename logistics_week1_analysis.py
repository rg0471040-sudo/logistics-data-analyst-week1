import pandas as pd

INPUT_FILE = "logistics_orders.csv"

df = pd.read_csv(INPUT_FILE)

print("Rows, columns:", df.shape)
print("\nMissing values:")
print(df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())

date_cols = ["order_date", "dispatch_date", "promised_date", "delivery_date"]
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

required = ["dispatch_date", "promised_date", "delivery_date"]
missing_required = [c for c in required if c not in df.columns]
if missing_required:
    raise ValueError(f"Missing required columns: {missing_required}")

df["delivery_days"] = (
    df["delivery_date"] - df["dispatch_date"]
).dt.total_seconds() / 86400

df["late_delivery"] = (
    df["delivery_date"] > df["promised_date"]
).astype("Int64")

on_time_rate = (1 - df["late_delivery"].mean()) * 100
avg_delivery_days = df["delivery_days"].mean()

print(f"\nOn-time delivery rate: {on_time_rate:.2f}%")
print(f"Average delivery time: {avg_delivery_days:.2f} days")

# Future extensions:
# 1. KPI analysis by route/warehouse/transport mode.
# 2. Feature engineering.
# 3. Regression/classification baseline.
# 4. Clustering where justified.
# 5. Inventory/resource allocation optimization.
