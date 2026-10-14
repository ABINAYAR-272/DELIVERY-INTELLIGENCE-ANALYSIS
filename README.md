# Delivery Intelligence: Delivery Delay Analysis

## 1. Project Overview

Delivery Intelligence is a data analytics project that examines shipment performance using the DataCo Smart Supply Chain dataset. It combines Python (pandas) for data cleaning, MYSQL for data validation and analysis with Power BI for interactive reporting.

The project compares actual shipping duration with scheduled shipping duration to measure delivery delays and identify patterns across shipping modes, regions, product categories, customer segments, cities, and order months.

## 2. Business Need

Delivery delays can negatively affect customer satisfaction, operational planning, and the reliability of delivery promises. Businesses need to understand how frequently shipments are late, how actual shipping duration compares with scheduled duration, and which segments have higher late-delivery rates.

This project converts shipment data into measurable KPIs and visual insights to support delivery-performance monitoring and further investigation.

The analysis identifies patterns and differences in delivery performance. It does not independently establish the causes of delays.


## 3. Key performance indicators

- **Total Shipment Records:** Total number of rows in the original dataset.
- **Valid Shipment Records:** Records containing both actual and scheduled shipping durations.
- **Late Shipment Records:** Valid records classified as Late.
- **Late-Delivery Rate:** Late records divided by valid-duration records, multiplied by 100.
- **Average Actual Shipping Days:** Average actual shipping duration among valid records.
- **Average Delay Days:** Average difference between actual and scheduled shipping duration.


## 4. Python Code Explanation

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

### Generated Output Files

The script creates the following files inside `delivery_outputs/`.

| File | Purpose |
|---|---|
| `kpi_summary.csv` | Overall delivery KPIs |
| `shipping_analysis.csv` | Analysis by shipping mode |
| `region_analysis.csv` | Analysis by order region |
| `category_analysis.csv` | Analysis by product category |
| `monthly_analysis.csv` | Monthly analysis by order month, when the date field is available |
| `delivery_cleaned.csv` | Cleaned dataset for Power BI |

## 5. SQL Analysis

SQL complemented Python and Power BI by adding data validation and deeper analysis of delivery risks and customer ordering patterns.

### 1. Data Quality Checks
- Checked duplicates, missing values, invalid shipping durations, and status inconsistencies.

**Business value:** Improves data reliability.

### 2. Regional Risk Ranking
- Used CTEs and `DENSE_RANK()` to rank regions by late-delivery rate within each market, excluding groups with fewer than 100 records.

**Business value:** Helps prioritize regional investigations.

### 3. High-Risk Combinations
- Analyzed market, region, shipping mode, and product category combinations to identify groups with elevated late-delivery rates.

**Business value:** Highlights operational segments for further investigation.

### 4. Customer and Order Analysis
- Analyzed distinct order frequency, repeat ordering, and customer-level late-delivery rates.

**Business value:** Provides insights into customer ordering patterns and delivery experience.

## 6. POWERBI Dashboard

### Page 1: Delivery Overview

This dashboard provides an overview of shipment records, profit, average shipping duration, late-delivery rate, city-level performance, and delivery status.

<img width="665" height="400" alt="PAGE 1" src="https://github.com/user-attachments/assets/f174c1f8-5dad-48c4-9569-e040c994553a" />

### Page 2: Delivery Performance Analysis

This dashboard compares late-delivery rates across product categories, regions, shipping modes, and customer segments

<img width="660" height="376" alt="PAGE 2" src="https://github.com/user-attachments/assets/d1038b08-2720-423d-8007-0999df953424" />


## 7. Technologies Used

- **Python:** Analysis workflow and data processing.
- **MYSQL:** data quality validation,investigation of high-risk combinations, and customer ordering patterns.
- **pandas:** Data cleaning, grouping, calculations, and CSV exports.
- **Power BI Desktop:** KPI cards, charts, and report visualization.
- **Git and GitHub:** Version control and project documentation.

### Requirements

- Python 3.9 or later, or another compatible Python version.
- pandas.
- MYSQL 8 and MYSQL workbench.
- The DataCo CSV dataset.
- Power BI Desktop to open the report.


## 8. Suggested Repository Structure

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
