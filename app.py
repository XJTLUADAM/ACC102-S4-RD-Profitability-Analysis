import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels import PanelOLS
from statsmodels.tools.tools import add_constant

# 页面设置
st.set_page_config(page_title="R&D & ROA Dashboard", layout="wide")
plt.style.use('seaborn-v0_8')

# --------------------------
# 1. 加载数据
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_data.csv")
    return df

df = load_data()

# --------------------------
# 👈 左边加时间筛选（你要的调时间功能）
# --------------------------
min_year = int(df['fyear'].min())
max_year = int(df['fyear'].max())

st.sidebar.header("⚙️ Filter")
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# 按筛选后的时间过滤数据
df_filtered = df[(df['fyear'] >= selected_years[0]) & (df['fyear'] <= selected_years[1])]

# --------------------------
# 页面标签
# --------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Data Overview", 
    "📈 Descriptive Statistics", 
    "🔍 Correlation Analysis", 
    "📉 Regression & Results"
])

# --------------------------
# Tab1 数据概览
# --------------------------
with tab1:
    st.header("Data Overview (Filtered)")
    st.dataframe(df_filtered.head(10), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Observations", len(df_filtered))
    col2.metric("Firms", df_filtered['gvkey'].nunique())
    col3.metric("Selected Years", f"{selected_years[0]}–{selected_years[1]}")

    st.divider()
    st.subheader("Yearly Trend (R&D & ROA)")
    st.image("output/03_yearly_trend.png", use_column_width=True)

# --------------------------
# Tab2 描述统计
# --------------------------
with tab2:
    st.header("Descriptive Statistics")
    desc = pd.read_csv("output/descriptive_statistics.csv", index_col=0)
    st.dataframe(desc, use_container_width=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.image("output/05_firm_size_distribution.png", use_column_width=True)
    with c2:
        st.image("output/01_rd_quintile_roa.png", use_column_width=True)

# --------------------------
# Tab3 相关性
# --------------------------
with tab3:
    st.header("Correlation Analysis")
    st.image("output/02_correlation_heatmap.png", use_column_width=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.image("output/04_rd_roa_scatter.png", use_column_width=True)
    with c2:
        st.image("output/06_leverage_roa.png", use_column_width=True)

# --------------------------
# Tab4 回归结果
# --------------------------
with tab4:
    st.header("Panel Regression (Two-Way Fixed Effects)")
    st.write("Dependent Variable: ROA")

    try:
        with open("output/regression_results.txt", "r", encoding="utf-8") as f:
            st.code(f.read(), language="text")
    except:
        df_reg = df_filtered.dropna(subset=["roa", "rd_intensity_lag1", "firm_size", "leverage"])
        model = PanelOLS.from_formula(
            "roa ~ 1 + rd_intensity_lag1 + firm_size + leverage + EntityEffects + TimeEffects",
            data=df_reg.set_index(["gvkey", "fyear"])
        )
        res = model.fit(cov_type="clustered", cluster_entity=True, check_rank=False)
        st.write(res.summary.tables[1].as_html(), unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    **Key Findings**  
    1. R&D intensity has a significant negative short-term effect on ROA.  
    2. Larger firms have higher profitability.  
    3. Higher leverage reduces firm profitability.
    """)