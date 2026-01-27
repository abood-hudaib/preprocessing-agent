# Data Preprocessing Agent

A client-ready Python tool that cleans and prepares messy CSV/Excel datasets for analysis, dashboards, or machine learning.

## The Problem
Most datasets contain:
- Missing values
- Duplicates
- Outliers
- Inconsistent formats
These issues slow analysis and lead to wrong decisions.

## The Solution
This tool provides an automated, configurable preprocessing pipeline that:
- Cleans data using Python (Pandas)
- Applies strategies defined in a config file
- Produces a clean dataset + a clear preprocessing report

## What You Get
- `cleaned_data.csv` or `cleaned_data.xlsx`
- `report.md` with before/after metrics

## Features
- CSV / Excel support
- Robust CSV loading (encoding & separator handling)
- Missing values handling (mean/median/constant/drop)
- Duplicate removal
- Outlier handling (IQR)
- Numeric scaling (Standard / MinMax)
- Client-friendly preprocessing report

## How to Run
```bash
python main.py --input your_data.csv --config config.yml --output outputs
