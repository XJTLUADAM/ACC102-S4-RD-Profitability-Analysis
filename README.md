# R&D Investment and Profitability Analysis Tool
This is an interactive data analysis tool for ACC102 Mini Assignment Track 4.

## Project Introduction
This tool examines the impact of R&D investment on firm profitability for US public firms (2018-2023). It provides interactive visualizations and empirical regression results to help investors understand the value of R&D investment.

## Data Source
Data is obtained from WRDS Compustat, accessed on 23 April 2026. We exclude financial and utility firms, and apply 1% winsorization to eliminate outliers.

## Project Structure
- `01_wrds_data_fetch.py`: Script to fetch raw financial data from WRDS database
- `02_data_cleaning.py`: Script to clean raw data, handle missing values, and construct core variables
- `03_run_analysis.py`: Script to run descriptive statistics and panel regression analysis
- `04_generate_plots.py`: Script to generate visualization charts for analysis results
- `acc102 finally.ipynb`: Full end-to-end analytical workflow Jupyter Notebook
- `app.py`: Core code of the Streamlit interactive application
- `requirements.txt`: List of all required Python dependencies
- `raw_compustat.csv`: Raw financial dataset from WRDS
- `processed_data.csv`: Cleaned and processed final dataset for analysis

## How to Run Locally
1. Install all required dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py