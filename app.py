# R&D Investment and Corporate Profitability Analysis
# ACC102 Mini Assignment - Track 4: Interactive Data Analysis Tool
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------- 环境适配（避免Matplotlib报错）--------------------------
plt.rcParams['axes.unicode_minus'] = False
plt.switch_backend('Agg')

# -------------------------- 页面基础配置 --------------------------
st.set_page_config(
    page_title="R&D & Profitability Analysis | ACC102",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 侧边栏 --------------------------
with st.sidebar:
    st.title("📌 Menu")
    menu = st.radio(
        "Go to",
        ["Project Overview", "Data Overview", "Descriptive Statistics", "Correlation Analysis", "Regression Results", "Visualization Charts"]
    )
    st.markdown("---")
    st.markdown("**ACC102 Mini Assignment**")
    st.markdown("Track 4 • Streamlit Interactive Tool")
    st.markdown("Topic: R&D Intensity vs Firm ROA")

# -------------------------- 1. 项目介绍（作业要求：Problem Definition）--------------------------
if menu == "Project Overview":
    st.title("📈 R&D Investment and Corporate Profitability Analysis")
    st.subheader("ACC102 - Track 4: Interactive Data Analysis Tool")
    st.markdown("""
    ### Analytical Purpose
    This project explores the relationship between **R&D intensity** and corporate profitability (ROA) 
    using U.S. public firm data from 2018 to 2023.

    ### Research Questions
    1. What is the impact of lagged R&D intensity on firm ROA?
    2. How do firm size and leverage affect profitability?
    3. What are the trends of R&D investment and corporate performance over time?

    ### Data Source
    - WRDS Compustat Fundamental Annual (2018–2023)
    - U.S. public firms, excluding financial & utility industries
    """)
    st.success("✅ This interactive tool supports result viewing & analysis presentation.")

# -------------------------- 2. 数据概览 --------------------------
elif menu == "Data Overview":
    st.title("📋 Data Overview")
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/processed_data.csv")
        return df
    df = load_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observations", len(df))
    col2.metric("Unique Firms", df['gvkey'].nunique())
    col3.metric("Year Range", f"{df['fyear'].min()}–{df['fyear'].max()}")

    st.markdown("### Sample Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("### Key Variables")
    st.code("""
    roa: Return on Assets (net income / assets)
    rd_intensity: R&D / Assets
    rd_intensity_lag1: Lagged R&D intensity
    firm_size: Log(Total Assets)
    leverage: (Short-term + Long-term debt) / Assets
    """)

# -------------------------- 3. 描述性统计 --------------------------
elif menu == "Descriptive Statistics":
    st.title("📊 Descriptive Statistics")
    df = pd.read_csv("data/processed_data.csv")
    desc_vars = ["roa", "rd_intensity", "rd_intensity_lag1", "firm_size", "leverage"]
    desc_table = df[desc_vars].describe().round(4)
    st.dataframe(desc_table, use_container_width=True)

# -------------------------- 4. 相关性分析 --------------------------
elif menu == "Correlation Analysis":
    st.title("🔗 Correlation Analysis")
    df = pd.read_csv("data/processed_data.csv")
    corr_vars = ["roa", "rd_intensity_lag1", "firm_size", "leverage"]
    corr_matrix = df[corr_vars].corr().round(4)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Correlation Matrix")
        st.dataframe(corr_matrix, use_container_width=True)
    with col2:
        st.markdown("### Heatmap")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=ax)
        st.pyplot(fig)

# -------------------------- 5. 回归结果 --------------------------
elif menu == "Regression Results":
    st.title("📉 Panel Regression Results")
    try:
        with open("output/regression_results.txt", "r", encoding="utf-8") as f:
            reg_result = f.read()
        st.text(reg_result)
    except:
        st.error("Please run 03_analysis.py first to generate regression results.")

# -------------------------- 6. 可视化图表 --------------------------
elif menu == "Visualization Charts":
    st.title("📊 Visualization Charts")
    chart_info = [
        ("output/01_rd_quintile_roa.png", "R&D Quintile vs Average ROA"),
        ("output/02_correlation_heatmap.png", "Correlation Heatmap"),
        ("output/03_yearly_trend.png", "Yearly Trend: R&D & ROA"),
        ("output/04_rd_roa_scatter.png", "R&D Intensity vs ROA Fitting"),
        ("output/05_firm_size_distribution.png", "Firm Size Distribution"),
        ("output/06_leverage_roa.png", "Leverage Quartile vs ROA")
    ]

    for i in range(0, 6, 3):
        row = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < 6:
                with row[j]:
                    st.markdown(f"#### {chart_info[idx][1]}")
                    try:
                        st.image(chart_info[idx][0], use_column_width=True)
                    except:
                        st.warning("Chart missing: run 04_visualization.py")

st.markdown("---")
st.caption("© ACC102 2025-26 S2 • Track 4 Interactive Data Tool")