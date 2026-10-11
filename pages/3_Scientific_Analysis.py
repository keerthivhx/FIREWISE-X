"""
Page 3: Scientific Analysis
Interactive exploration of physical combustion relationships, correlations, and comparative statistics.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile
from components.source_status import render_source_status_banner
from components.charts import (
    create_scatter_plot,
    create_histogram,
    create_box_plot,
    create_correlation_heatmap
)
from src.analysis.descriptive import DescriptiveAnalyzer
from src.analysis.trends import TrendAnalyzer

st.set_page_config(page_title="Scientific Analysis | FIREWISE-X", page_icon="📈", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("📈 Scientific Analysis Engine")
st.markdown("Examine empirical combustion kinetics, correlation matrices, and parametric distributions.")

if "active_df" not in st.session_state or st.session_state.active_df.empty:
    st.warning("No active dataset loaded. Please navigate to the main Dashboard first.")
    st.stop()

df = st.session_state.active_df
meta = st.session_state.active_meta

render_source_status_banner(meta)

# Discover available numeric and categorical features dynamically
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

if not num_cols:
    st.info("The active dataset is documentary/qualitative and lacks continuous numeric fields.")
    if cat_cols:
        st.markdown("### 📊 Categorical Frequency Distribution")
        sel_cat = st.selectbox("Select Categorical Feature", options=cat_cols)
        counts = df[sel_cat].value_counts().reset_index()
        counts.columns = [sel_cat, "count"]
        fig = create_scatter_plot(counts, x_col=sel_cat, y_col="count", title=f"Frequency Distribution: {sel_cat}")
        st.plotly_chart(fig, use_container_width=True)
    st.stop()

# Tabbed Analysis Interface
tab_corr, tab_dist, tab_group, tab_bivariate = st.tabs([
    "🔗 Correlation Matrix",
    "📊 Variable Distributions",
    "👥 Group Comparisons",
    "🎯 Bivariate Scatter & Trendline"
])

# Tab 1: Correlation Matrix
with tab_corr:
    st.markdown("### 🔗 Inter-Variable Correlation Structure")
    corr_results = TrendAnalyzer.compute_correlations(df)
    if corr_results.get("has_correlations"):
        p_df = pd.DataFrame(corr_results["pearson_matrix"])
        fig_heat = create_correlation_heatmap(p_df, title="Pearson Correlation Heatmap (Linear Covariation)")
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("#### 🔍 Strongest Empirical Covariance Pairs:")
        top_pairs = corr_results.get("top_correlations", [])[:4]
        if top_pairs:
            pair_cols = st.columns(len(top_pairs))
            for p_idx, pair in enumerate(top_pairs):
                r_val = pair['pearson_r']
                r_color = "#00d2ff" if r_val > 0 else "#ff6b4a"
                with pair_cols[p_idx]:
                    st.markdown(
                        f"""
                        <div class="glass-card">
                            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Pair #{p_idx+1}</div>
                            <div style="color: {r_color}; font-size: 1.5rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 2px 0;">
                                r = {r_val:+.2f}
                            </div>
                            <div style="font-size: 0.75rem; color: #cbd5e1;">{pair['var1']} <br>vs. {pair['var2']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.info(corr_results.get("reason", "Correlations cannot be calculated."))

# Tab 2: Variable Distributions
with tab_dist:
    st.markdown("### 📊 Univariate Distribution & Dispersion")
    selected_num = st.selectbox("Select Target Variable to Inspect", options=num_cols)
    c1, c2 = st.columns([13, 7])

    with c1:
        fig_hist = create_histogram(
            df,
            col=selected_num,
            color_col="fuel_category" if "fuel_category" in df.columns else None,
            title=f"Parametric Distribution: {selected_num}"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        s = df[selected_num].dropna()
        q25 = float(s.quantile(0.25))
        q75 = float(s.quantile(0.75))
        iqr = q75 - q25

        st.markdown(
            f"""
            <div class="glass-card" style="margin-top: 15px;">
                <h4 style="color: #00d2ff; margin-top: 0; font-size: 1rem;">Statistical Summary: <code>{selected_num}</code></h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-family: 'JetBrains Mono'; font-size: 0.85rem;">
                    <div><span style="color:#64748b;">Count:</span> {int(s.count()):,}</div>
                    <div><span style="color:#64748b;">Mean:</span> {float(s.mean()):.3f}</div>
                    <div><span style="color:#64748b;">Median:</span> {float(s.median()):.3f}</div>
                    <div><span style="color:#64748b;">Std Dev:</span> {float(s.std()):.3f}</div>
                    <div><span style="color:#64748b;">Min:</span> {float(s.min()):.3f}</div>
                    <div><span style="color:#64748b;">Max:</span> {float(s.max()):.3f}</div>
                    <div><span style="color:#64748b;">Q25:</span> {q25:.3f}</div>
                    <div><span style="color:#64748b;">Q75:</span> {q75:.3f}</div>
                    <div><span style="color:#64748b;">IQR:</span> {iqr:.3f}</div>
                    <div><span style="color:#64748b;">Nulls:</span> {int(df[selected_num].isna().sum())}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Tab 3: Group Comparisons
with tab_group:
    st.markdown("### 👥 Comparative Analysis by Experimental Category")
    if cat_cols:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            grp_col = st.selectbox("Grouping Attribute", options=cat_cols)
        with col_g2:
            metric_col = st.selectbox("Comparison Metric", options=num_cols)

        fig_box = create_box_plot(
            df,
            x_col=grp_col,
            y_col=metric_col,
            title=f"{metric_col} Stratified by {grp_col}"
        )
        st.plotly_chart(fig_box, use_container_width=True)

        grp_stats = TrendAnalyzer.analyze_by_group(df, group_col=grp_col, metric_cols=[metric_col])
        if grp_stats.get("valid"):
            st.markdown("#### Aggregated Statistics by Group:")
            st.dataframe(pd.DataFrame(grp_stats["summary_table"]), use_container_width=True)
    else:
        st.info("No categorical features available for grouping in this dataset.")

# Tab 4: Custom Bivariate Scatter & Trendline
with tab_bivariate:
    st.markdown("### 🎯 Custom Bivariate Exploration with OLS Regression")
    col_x, col_y, col_c, col_t = st.columns([1, 1, 1, 1])
    with col_x:
        x_var = st.selectbox("X-Axis Feature", options=num_cols, index=0)
    with col_y:
        y_var = st.selectbox("Y-Axis Feature", options=num_cols, index=min(1, len(num_cols) - 1))
    with col_c:
        color_choices = ["None"] + cat_cols + num_cols
        c_var = st.selectbox("Color Dimension", options=color_choices)
    with col_t:
        st.write("")
        st.write("")
        add_trend = st.checkbox("Show OLS Trendline", value=True)

    fig_custom = create_scatter_plot(
        df,
        x_col=x_var,
        y_col=y_var,
        color_col=None if c_var == "None" else c_var,
        hover_name="test_id" if "test_id" in df.columns else None,
        title=f"Parametric Relationship: {y_var} vs. {x_var}",
        add_trendline=add_trend
    )
    st.plotly_chart(fig_custom, use_container_width=True)
