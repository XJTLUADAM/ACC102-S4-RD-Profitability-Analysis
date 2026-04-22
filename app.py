import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels import PanelOLS

# 页面基础配置
st.set_page_config(
    page_title="R&D & Profitability Analysis",
    page_icon="📊",
    layout="wide"
)

# 全局绘图设置
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'Arial'

# --------------------------
# 加载数据（缓存，只加载一次）
# --------------------------
@st.cache_data
def load_data():
    # 读取你项目里的处理后数据
    df = pd.read_csv('data/processed_data.csv')
    return df

df = load_data()

# --------------------------
# 侧边栏（交互筛选）
# --------------------------
st.sidebar.title("📊 R&D Investment & Profitability Tool")
st.sidebar.markdown("---")
st.sidebar.markdown("**ACC102 Track 4 Interactive Assignment**")

# 年份筛选器
year_min = int(df['fyear'].min())
year_max = int(df['fyear'].max())
selected_year = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# 应用筛选
df_filtered = df[(df['fyear'] >= selected_year[0]) & (df['fyear'] <= selected_year[1])]

# --------------------------
# 主页面标题
# --------------------------
st.title("R&D Investment and Firm Profitability Analysis")
st.markdown("### Evidence from US Listed Companies (2018-2023)")
st.markdown("---")

# --------------------------
# 标签页
# --------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Data Overview",
    "📊 Descriptive Statistics",
    "🔍 Correlation Analysis",
    "📈 Regression & Visualizations"
])

# 标签页1：数据概览
with tab1:
    st.subheader("Sample Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observations", len(df_filtered))
    col2.metric("Average ROA", f"{df_filtered['roa'].mean():.3f}")
    col3.metric("Average R&D Intensity", f"{df_filtered['rd_intensity'].mean():.3f}")
    
    st.subheader("Raw Data Preview")
    st.dataframe(df_filtered[['gvkey', 'fyear', 'roa', 'rd_intensity', 'firm_size', 'leverage']].head(10), use_container_width=True)

# 标签页2：描述性统计
with tab2:
    st.subheader("Descriptive Statistics (Core Variables)")
    desc_vars = ['roa', 'rd_intensity', 'rd_intensity_lag1', 'firm_size', 'leverage']
    desc_stats = df_filtered[desc_vars].describe().round(4)
    st.dataframe(desc_stats, use_container_width=True)

# 标签页3：相关性分析
with tab3:
    st.subheader("Correlation Matrix")
    corr_vars = ['roa', 'rd_intensity_lag1', 'firm_size', 'leverage']
    corr_matrix = df_filtered[corr_vars].corr().round(4)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', square=True)
    st.pyplot(fig)

# 标签页4：回归与可视化
with tab4:
    st.subheader("Panel Regression Results (Two-Way Fixed Effects)")
    with st.spinner("Running regression..."):
        # 运行回归
        df_reg = df_filtered.copy()
        df_reg['gvkey'] = df_reg['gvkey'].astype(str)
        df_reg['fyear'] = df_reg['fyear'].astype(int)
        df_reg = df_reg.set_index(['gvkey', 'fyear'])
        
        control_vars = [col for col in df_reg.columns if col.startswith(('industry_', 'fyear_')) or col in ['firm_size', 'leverage']]
        model = PanelOLS(df_reg['roa'], df_reg[['rd_intensity_lag1'] + control_vars], drop_absorbed=True)
        results = model.fit(cov_type='clustered', cluster_entity=True)
        
        st.text(str(results))
        
        # 核心结论
        rd_coef = results.params['rd_intensity_lag1']
        rd_pval = results.pvalues['rd_intensity_lag1']
        sig = "***" if rd_pval < 0.01 else "**" if rd_pval < 0.05 else "*" if rd_pval < 0.1 else "not significant"
        st.success(f"💡 Key Finding: A 1% increase in lagged R&D intensity is associated with a {rd_coef:.3f} change in ROA, {sig}.")

    st.subheader("Key Visualization: R&D vs ROA")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='rd_intensity_lag1', y='roa', data=df_filtered, scatter_kws={'alpha':0.3, 's':20}, line_kws={'color':'red', 'linewidth':2})
    plt.title('Lagged R&D Intensity vs ROA')
    st.pyplot(fig)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    ACC102 Mini Assignment - Track 4: Interactive Data Analysis Tool<br>
    Data Source: WRDS Compustat North America
</div>
""", unsafe_allow_html=True)