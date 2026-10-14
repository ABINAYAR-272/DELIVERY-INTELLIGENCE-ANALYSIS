# Delivery Intelligence: Delivery Delay Analysis

## 1. Project Overview

Delivery Intelligence is a data analytics project that examines shipment performance using the DataCo Smart Supply Chain dataset. It combines Python (pandas) for data cleaning and analysis with Power BI for interactive reporting.

The project compares actual shipping duration with scheduled shipping duration to measure delivery delays and identify patterns across shipping modes, regions, product categories, customer segments, cities, and order months.

## 2. Business Need

Delivery delays can negatively affect customer satisfaction, operational planning, and the reliability of delivery promises. Businesses need to understand how frequently shipments are late, how actual shipping duration compares with scheduled duration, and which segments have higher late-delivery rates.

This project converts shipment data into measurable KPIs and visual insights to support delivery-performance monitoring and further investigation.

The analysis identifies patterns and differences in delivery performance. It does not independently establish the causes of delays.

## 3. Project Objectives

- Measure total shipment records and valid shipping-duration records.
- Calculate late shipment records and late-delivery rate.
- Calculate average actual shipping duration and delivery delay.
- Compare performance across shipping modes, regions, and product categories.
- Examine differences across customer segments and cities in Power BI.
- Analyze monthly delivery patterns using order dates.
- Present key metrics through an interactive Power BI report.

## 4. Project Scope

- Loading and validating the dataset using pandas.
- Converting shipping-duration columns to numeric values.
- Handling missing or invalid shipping-duration values.
- Calculating delay days and classifying valid records as Early, On Time, or Late.
- Calculating overall delivery KPIs.
- Grouping and comparing delivery performance by shipping mode, region, and category.
- Producing monthly summary data when the order-date field is available.
- Exporting CSV files for Power BI.
- Visualizing delivery metrics and comparisons.


## 5. Dataset and KPI Definitions

The Python script expects `DataCoSupplyChainDataset.csv` and checks for these required columns:

- `Days for shipping (real)`
- `Days for shipment (scheduled)`
- `Shipping Mode`
- `Order Region`
- `Category Name`
- `Order Id`

The script also uses `order date (DateOrders)` when available.

### Derived fields

- `actual_shipping_days`: numeric conversion of actual shipping duration.
- `scheduled_shipping_days`: numeric conversion of scheduled shipping duration.
- `delay_days`: actual shipping duration minus scheduled shipping duration.
- `delivery_status_analysis`: delivery classification based on the calculated delay.

The classifications are:

- **Late:** Actual duration is greater than scheduled duration.
- **On Time:** Actual duration equals scheduled duration.
- **Early:** Actual duration is less than scheduled duration.

### Key performance indicators

- **Total Shipment Records:** Total number of rows in the original dataset.
- **Valid Shipment Records:** Records containing both actual and scheduled shipping durations.
- **Invalid Duration Records:** Records missing either duration after numeric conversion.
- **Late Shipment Records:** Valid records classified as Late.
- **Late-Delivery Rate:** Late records divided by valid-duration records, multiplied by 100.
- **Average Actual Shipping Days:** Average actual shipping duration among valid records.
- **Average Delay Days:** Average difference between actual and scheduled shipping duration.

**Metric limitation:** These calculations count rows, not distinct order IDs. An order appearing on multiple rows can contribute multiple times. Therefore, record-level KPIs should not be described as unique-order counts.

Monthly analysis groups by order month, not delivery-arrival month.

## 6. Python Code Explanation

The script `delivery_analysis.py` performs the following operations.

### Step 1: Configure file paths

Defines the project directory, source CSV location, and output directory. It creates the output directory automatically if needed.

### Step 2: Load the dataset

Uses pandas to read the CSV file with Latin-1 encoding and prints the number of rows and columns.

### Step 3: Validate required columns

Checks that essential shipping-duration and grouping columns exist. If required columns are missing, the script raises an error.

### Step 4: Clean shipping-duration data

Converts actual and scheduled shipping durations to numeric values. Values that cannot be converted become missing values.

Only records containing both durations are used for delivery-duration calculations.

### Step 5: Calculate delay and delivery status

Subtracts scheduled shipping duration from actual shipping duration and assigns an Early, On Time, or Late status.

### Step 6: Calculate overall KPIs

Calculates total records, valid and invalid records, late records, late-delivery rate, average actual shipping days, and average delay days.

Exports the results to `kpi_summary.csv`.

### Step 7: Analyze shipping modes

Groups valid records by shipping mode and calculates shipment counts, late counts, late-delivery rates, and average shipping durations.

Exports `shipping_analysis.csv`.

### Step 8: Analyze regions

Groups valid records by order region and calculates late-delivery and duration metrics.

Exports `region_analysis.csv`.

### Step 9: Analyze product categories

Groups valid records by product category and calculates late-delivery and duration metrics.

Exports `category_analysis.csv`.

### Step 10: Analyze monthly trends

When the order-date field is available, parses the dates and groups valid records by order month.

Exports `monthly_analysis.csv`.

### Step 11: Export cleaned data

Creates `delivery_cleaned.csv`, retaining the original columns and adding the calculated `delay_days` and `delivery_status_analysis` fields.

### Step 12: Report completion

Prints the output directory and lists the generated CSV files.

## 7. Generated Output Files

The script creates the following files inside `delivery_outputs/`.

| File | Purpose |
|---|---|
| `kpi_summary.csv` | Overall delivery KPIs |
| `shipping_analysis.csv` | Analysis by shipping mode |
| `region_analysis.csv` | Analysis by order region |
| `category_analysis.csv` | Analysis by product category |
| `monthly_analysis.csv` | Monthly analysis by order month, when the date field is available |
| `delivery_cleaned.csv` | Cleaned dataset for Power BI |

## 8. Technologies Used

- **Python:** Analysis workflow and data processing.
- **pandas:** Data cleaning, grouping, calculations, and CSV exports.
- **Power BI Desktop:** KPI cards, charts, and report visualization.
- **Git and GitHub:** Version control and project documentation.

## 9. How to Run the Project

### Requirements

- Python 3.9 or later, or another compatible Python version.
- pandas.
- The DataCo CSV dataset.
- Power BI Desktop to open the report.

Install pandas:

```bash
python -m pip install pandas
```

### Run the Python script

1. Place `delivery_analysis.py` and `DataCoSupplyChainDataset.csv` in the expected project directory.
2. Update the configured path if necessary.
3. Open a terminal in that directory.
4. Run:

```bash
python delivery_analysis.py
```

5. Check the `delivery_outputs` folder for the generated CSV files.
6. Open `Delivery_Delay_Analysis.pbix` in Power BI Desktop and refresh its data source if the files have moved.

The current script uses this Windows-specific path:

```python
BASE_DIR = Path(r"D:\DATA ANALYTICS\PROJECTS\DELIVERY_INTELLIGENCE_PROJECT")
```

Change it to match the directory on your computer.

## 10. POWERBI Dashboard

Page 1: Delivery Overview

This dashboard provides an overview of shipment records, profit, average shipping duration, late-delivery rate, city-level performance, and delivery status.

<img width="668" height="380" alt="Screenshot 2026-10-14 095605" src="https://github.com/user-attachments/assets/abbd02ae-0d29-40fa-9cf6-3f4081b51928" />


Page 2: Delivery Performance Analysis

This dashboard compares late-delivery rates across product categories, regions, shipping modes, and customer segments

<img width="664" height="374" alt="Screenshot 2026-10-14 095630" src="https://github.com/user-attachments/assets/ae6ec320-5411-43e7-ad62-d93e98f42d4b" />



## Suggested Repository Structure

```text
delivery-intelligence/
├── README.md
├── delivery_analysis.py
├── Delivery_Delay_Analysis.pbix
├── data/
│   └── DataCoSupplyChainDataset.csv
└── delivery_outputs/
    ├── kpi_summary.csv
    ├── shipping_analysis.csv
    ├── region_analysis.csv
    ├── category_analysis.csv
    ├── monthly_analysis.csv
    └── delivery_cleaned.csv
```
