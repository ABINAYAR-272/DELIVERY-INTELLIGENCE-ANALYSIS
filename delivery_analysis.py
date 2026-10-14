
import pandas as pd
from pathlib import Path

# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = Path(r"D:\DATA ANALYTICS\PROJECTS\DELIVERY_INTELLIGENCE_PROJECT")

DATA_FILE = BASE_DIR / "DataCoSupplyChainDataset.csv"

# Create output folder automatically
OUTPUT_DIR = BASE_DIR / "delivery_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_FILE, encoding="latin-1", low_memory=False)

print("\nDataset loaded successfully.")
print(f"Original dataset rows: {len(df):,}")
print(f"Original dataset columns: {len(df.columns):,}")

# ============================================================
# 3. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Shipping Mode",
    "Order Region",
    "Category Name",
    "Order Id",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(
        "Missing required columns: " + ", ".join(missing_columns)
    )

# ============================================================
# 4. CLEAN SHIPPING DATA
# ============================================================

df["actual_shipping_days"] = pd.to_numeric(
    df["Days for shipping (real)"], errors="coerce"
)

df["scheduled_shipping_days"] = pd.to_numeric(
    df["Days for shipment (scheduled)"], errors="coerce"
)

# Only include records with both shipping durations available
valid = df[
    df["actual_shipping_days"].notna()
    & df["scheduled_shipping_days"].notna()
].copy()

# Calculate delivery delay
valid["delay_days"] = (
    valid["actual_shipping_days"]
    - valid["scheduled_shipping_days"]
)

# Classify delivery status
valid["delivery_status_analysis"] = "On Time"

valid.loc[
    valid["delay_days"] > 0,
    "delivery_status_analysis"
] = "Late"

valid.loc[
    valid["delay_days"] < 0,
    "delivery_status_analysis"
] = "Early"

# Helper function
def calculate_late_rate(status_series):
    if len(status_series) == 0:
        return 0.0
    return (status_series == "Late").mean() * 100

# ============================================================
# 5. OVERALL DELIVERY KPIs
# ============================================================

total_shipment_records = len(df)
valid_shipment_records = len(valid)
invalid_duration_records = len(df) - len(valid)

late_shipment_records = (
    valid["delivery_status_analysis"] == "Late"
).sum()

late_delivery_rate = (
    late_shipment_records / valid_shipment_records * 100
    if valid_shipment_records > 0
    else 0.0
)

average_actual_shipping_days = valid["actual_shipping_days"].mean()
average_delay_days = valid["delay_days"].mean()

print("\n" + "=" * 60)
print("OVERALL DELIVERY KPIs")
print("=" * 60)

print(f"Total shipment records: {total_shipment_records:,}")
print(f"Valid-duration records: {valid_shipment_records:,}")
print(f"Invalid-duration records: {invalid_duration_records:,}")
print(f"Late shipment records: {late_shipment_records:,}")
print(f"Late-delivery rate: {late_delivery_rate:.2f}%")

if pd.notna(average_actual_shipping_days):
    print(f"Average actual shipping days: {average_actual_shipping_days:.2f}")
else:
    print("Average actual shipping days: N/A")

if pd.notna(average_delay_days):
    print(f"Average delay days: {average_delay_days:.2f}")
else:
    print("Average delay days: N/A")

# Export KPI summary
kpi_summary = pd.DataFrame([
    {"KPI": "Total shipment records", "Value": total_shipment_records},
    {"KPI": "Valid-duration records", "Value": valid_shipment_records},
    {"KPI": "Invalid-duration records", "Value": invalid_duration_records},
    {"KPI": "Late shipment records", "Value": int(late_shipment_records)},
    {"KPI": "Late-delivery rate (%)", "Value": late_delivery_rate},
    {
        "KPI": "Average actual shipping days",
        "Value": average_actual_shipping_days,
    },
    {"KPI": "Average delay days", "Value": average_delay_days},
])

kpi_summary.to_csv(OUTPUT_DIR / "kpi_summary.csv", index=False)

# ============================================================
# 6. SHIPPING MODE ANALYSIS
# ============================================================

shipping_mode_analysis = (
    valid.groupby("Shipping Mode", dropna=False)
    .agg(
        shipment_records=("delivery_status_analysis", "size"),
        late_shipment_records=(
            "delivery_status_analysis",
            lambda s: (s == "Late").sum(),
        ),
        late_rate_pct=("delivery_status_analysis", calculate_late_rate),
        average_actual_days=("actual_shipping_days", "mean"),
        average_scheduled_days=("scheduled_shipping_days", "mean"),
        average_delay_days=("delay_days", "mean"),
    )
    .reset_index()
    .sort_values("late_rate_pct", ascending=False)
)

print("\n" + "=" * 60)
print("LATE RATE BY SHIPPING MODE")
print("=" * 60)
print(shipping_mode_analysis.round(2).to_string(index=False))

shipping_mode_analysis.to_csv(
    OUTPUT_DIR / "shipping_analysis.csv", index=False
)

# ============================================================
# 7. REGIONAL ANALYSIS
# ============================================================

region_analysis = (
    valid.groupby("Order Region", dropna=False)
    .agg(
        shipment_records=("delivery_status_analysis", "size"),
        late_shipment_records=(
            "delivery_status_analysis",
            lambda s: (s == "Late").sum(),
        ),
        late_rate_pct=("delivery_status_analysis", calculate_late_rate),
        average_actual_days=("actual_shipping_days", "mean"),
        average_delay_days=("delay_days", "mean"),
    )
    .reset_index()
    .sort_values("late_rate_pct", ascending=False)
)

print("\n" + "=" * 60)
print("LATE RATE BY REGION")
print("=" * 60)
print(region_analysis.round(2).to_string(index=False))

region_analysis.to_csv(
    OUTPUT_DIR / "region_analysis.csv", index=False
)

# ============================================================
# 8. PRODUCT CATEGORY ANALYSIS
# ============================================================

category_analysis = (
    valid.groupby("Category Name", dropna=False)
    .agg(
        shipment_records=("delivery_status_analysis", "size"),
        late_shipment_records=(
            "delivery_status_analysis",
            lambda s: (s == "Late").sum(),
        ),
        late_rate_pct=("delivery_status_analysis", calculate_late_rate),
        average_actual_days=("actual_shipping_days", "mean"),
        average_delay_days=("delay_days", "mean"),
    )
    .reset_index()
    .sort_values("late_rate_pct", ascending=False)
)

print("\n" + "=" * 60)
print("LATE RATE BY PRODUCT CATEGORY")
print("=" * 60)
print(category_analysis.round(2).to_string(index=False))

category_analysis.to_csv(
    OUTPUT_DIR / "category_analysis.csv", index=False
)

# ============================================================
# 9. MONTHLY DELIVERY TREND
# ============================================================

if "order date (DateOrders)" in df.columns:
    df["order_date"] = pd.to_datetime(
        df["order date (DateOrders)"],
        errors="coerce",
    )

    monthly_data = valid.copy()
    monthly_data["order_date"] = df.loc[valid.index, "order_date"]
    monthly_data = monthly_data.dropna(subset=["order_date"])

    monthly_data["order_month"] = (
        monthly_data["order_date"].dt.to_period("M").astype(str)
    )

    monthly_analysis = (
        monthly_data.groupby("order_month")
        .agg(
            shipment_records=("delivery_status_analysis", "size"),
            late_shipment_records=(
                "delivery_status_analysis",
                lambda s: (s == "Late").sum(),
            ),
            late_rate_pct=(
                "delivery_status_analysis",
                calculate_late_rate,
            ),
            average_actual_days=("actual_shipping_days", "mean"),
            average_delay_days=("delay_days", "mean"),
        )
        .reset_index()
        .sort_values("order_month")
    )

    print("\n" + "=" * 60)
    print("MONTHLY DELIVERY TREND")
    print("=" * 60)
    print(monthly_analysis.round(2).to_string(index=False))

    monthly_analysis.to_csv(
        OUTPUT_DIR / "monthly_analysis.csv", index=False
    )

# ============================================================
# 10. EXPORT CLEANED DATA FOR POWER BI
# ============================================================

cleaned_output = df.copy()

cleaned_output["delay_days"] = pd.NA
cleaned_output["delivery_status_analysis"] = pd.NA

cleaned_output.loc[valid.index, "delay_days"] = valid["delay_days"]

cleaned_output.loc[
    valid.index, "delivery_status_analysis"
] = valid["delivery_status_analysis"]

cleaned_output.to_csv(
    OUTPUT_DIR / "delivery_cleaned.csv", index=False
)

# ============================================================
# 11. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"Output folder: {OUTPUT_DIR}")
print("\nFiles created:")

for output_file in sorted(OUTPUT_DIR.glob("*.csv")):
    print(f"- {output_file.name}")

print("\nImport these CSV files into Power BI for your dashboard.")
