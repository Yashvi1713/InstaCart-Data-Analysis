# Instacart Retail Analytics Platform — Design Document

## Project Objective
Build an enterprise-style retail analytics platform using Python, Snowflake, SQL, and Power BI.

## Dataset
Instacart Market Basket Analysis dataset.

## Current Architecture

Raw CSV Files
→ Python Profiling Pipeline
→ Profiling Reports
→ Data Dictionary
→ Validation Rules
→ Cleaning/Transformation
→ Snowflake Warehouse
→ Power BI Dashboard

## Work Completed So Far

### 1. Project Setup
- Created Python virtual environment.
- Created modular project structure.
- Added `python_etl` package structure.
- Added profiling and utility modules.

### 2. Raw Data Ingestion Setup
- Stored raw Instacart CSV files under `data/raw`.
- Confirmed 6 CSV files are detected by the profiling pipeline.

### 3. Logging Framework
- Created reusable logger.
- Logs pipeline execution under `logs/profiling_pipeline.log`.

### 4. Data Profiling Framework
- Built reusable profiling functions.
- Generated column-level profiling reports.
- Generated dataset-level summary reports.

### 5. Profiling Outputs
Generated reports include:
- file name
- column name
- data type
- row count
- null count
- null percentage
- duplicate count
- unique count
- sample values
- dataset memory usage
- duplicate row count

## Key Profiling Findings
- Most tables have zero nulls.
- Duplicate values are expected in non-key columns such as `user_id`, `order_hour_of_day`, and foreign key columns.
- `days_since_prior_order` contains expected nulls for first customer orders.
- Dataset appears relatively clean, so validation and transformation will be more important than heavy cleaning.

## Next Steps

### Step 1: Data Dictionary
Create a business and technical data dictionary from profiling reports.

### Step 2: Validation Rules
Define rules for:
- primary keys
- foreign keys
- allowed value ranges
- allowed categorical values
- referential integrity

### Step 3: Validation Framework
Build Python validation scripts and generate validation reports.

### Step 4: Transformation Layer
Merge `order_products__prior` and `order_products__train` into one analytical order items table.

### Step 5: Warehouse Modeling
Design fact and dimension tables for Snowflake.

## Target Gold Layer Tables
- fact_order_items
- dim_products
- dim_departments
- dim_aisles
- dim_users
- dim_order_time

## Tools
- Python
- Pandas
- Pathlib
- Logging
- Snowflake
- Power BI
- GitHub