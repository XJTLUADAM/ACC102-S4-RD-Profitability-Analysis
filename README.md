# R&D Investment and Profitability Analysis Tool
This is an interactive data analysis tool for ACC102 Mini Assignment Track 4.

## Project Introduction
This tool examines the impact of R&D investment on firm profitability for US public firms (2018-2023). It provides interactive visualizations and empirical regression results to help investors understand the value of R&D investment.

## Data Source
Data is obtained from WRDS Compustat, accessed on 23 April 2026. We exclude financial and utility firms, and apply 1% winsorization to eliminate outliers.

## Project Structure
- `01_wrds_data_fetch.py`: Script to fetch raw data from WRDS
- `02_data_cleaning.py`: Script to clean and process raw data
- `03_run_analysis.py`: Script to run panel regression analysis
- `04_generate_plots.py`: Script to generate visualization charts
- `analysis_workflow.ipynb`: Full analysis workflow notebook
- `SRC/app.py`: Streamlit interactive app code

## How to Run Locally
1. Install dependencies:
```bash
pip install -r requirements.txt
streamlit run SRC/app.py