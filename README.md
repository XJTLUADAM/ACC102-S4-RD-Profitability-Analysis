# R&D Investment and Profitability Analysis Dashboard
This is an interactive data analysis tool developed for ACC102 Mini Assignment Track 4. It explores the relationship between R&D investment and firm profitability based on U.S. public company data from 2018 to 2023.

## Project Overview
This project uses WRDS Compustat data to analyze how R&D intensity affects corporate profitability (ROA). The workflow includes data acquisition, cleaning, descriptive statistics, correlation analysis, visualization, and two-way fixed effects panel regression. The interactive dashboard presents all results clearly for users to view and understand key findings.

## Data Source
Data is obtained from WRDS Compustat database, accessed on 23 April 2026. Financial and utility firms are excluded, and 1% winsorization is applied to reduce the impact of extreme outliers.

## File Structure
- data/: Stores raw and cleaned data
  - raw_compustat_data.csv: Original data downloaded from WRDS
  - processed_data.csv: Cleaned data for analysis
- output/: Contains all charts and analysis results
  - 01_rd_quintile_roa.png: R&D intensity quintile and ROA comparison
  - 02_correlation_heatmap.png: Variable correlation heatmap
  - 03_yearly_trend.png: Annual trend of R&D intensity and ROA
  - 04_rd_roa_scatter.png: Scatter plot of R&D intensity and ROA
  - 05_firm_size_distribution.png: Firm size distribution
  - 06_leverage_roa.png: Leverage and ROA relationship
  - descriptive_statistics.csv: Descriptive statistics
  - correlation_matrix.csv: Correlation matrix
  - regression_results.txt: Panel regression results
- 01_wrds_data_fetch.py: Script to fetch data from WRDS
- 02_data_cleaning.py: Data cleaning and variable construction
- 03_run_analysis.py: Descriptive analysis and regression
- 04_generate_plots.py: Generate all visualization charts
- app.py: Main file of the Streamlit interactive dashboard
- requirements.txt: Required Python libraries

## How to Run Locally
1. Install required packages: pip install -r requirements.txt
2. Run the dashboard: streamlit run app.py

## Assignment Compliance
This project meets all requirements of ACC102 Track 4: complete Python data workflow, interactive visualization tool, clear analysis logic, compliant data source, and complete submission materials.