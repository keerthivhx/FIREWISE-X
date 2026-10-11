"""
Page 4: Anomaly Explorer
Unsupervised anomaly detection (Isolation Forest) and Tukey IQR outlier profiling with scientific interpretations.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile
from components.source_status import render_source_status_banner
from components.charts import create_anomaly_scatter
from src.analysis.anomalies import StatisticalAnomalyDetector
from src.ml.models import MicrogravityMLEngine

st.set_page_config(page_title="Anomaly Explorer | FIREWISE-X", page_icon="⚡", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("⚡ Anomaly & Outlier Explorer")
st.markdown("Discover multi-dimensional combustion outliers and explain their physical mechanisms.")

if "active_df" not in st.session_state or st.session_state.active_df.empty:
    st.warning("No active dataset loaded. Please navigate to the main Dashboard first.")
    st.stop()

df = st.session_state.active_df
meta = st.session_state.active_meta

render_source_status_banner(meta)

# Scientific Context Callout
st.markdown(
    """
    <div style="background: rgba(255, 107, 74, 0.08); border: 1px solid rgba(255, 107, 74, 0.3); 
                border-left: 4px solid #ff6b4a; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
        <strong style="color: #ff6b4a; font-size: 0.95rem;">🔬 Scientific Anomaly Interpretation:</strong>
        <p style="color: #cbd5e1; font-size: 0.88rem; margin: 4px 0 0 0; line-height: 1.5;">
            In microgravity combustion research, a mathematical anomaly <strong>does not imply an immediate fire hazard or spacecraft emergency</strong>. 
            Rather, it denotes rare experimental regimes: prolonged smoldering, boundary-layer quenching, or extreme oxidizer flow velocities.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if len(num_cols) < 2:
    st.warning("Anomaly exploration requires at least two numeric physical dimensions.")
    st.stop()

method_tabs = st.tabs(["🌲 Multi-Dimensional Isolation Forest", "📏 Univariate Statistical (IQR) Profiler"])

# Tab 1: Isolation Forest
with method_tabs[0]:
    st.markdown("### 🌲 Unsupervised Multi-Dimensional Isolation Forest")
    st.markdown(
        "Fits an ensemble of 100 Isolation Trees to partition parameter space. "
        "Observations with shallow average path lengths represent rare physical operating states."
    )

    c_feat, c_cont = st.columns([3, 1])
    with c_feat:
        default_features = [c for c in num_cols if not c.startswith("_")][:5]
        chosen_features = st.multiselect(
            "Select Physical Features for Model Training",
            options=num_cols,
            default=default_features
        )
    with c_cont:
        contamination = st.slider("Contamination Ratio (Expected Outlier Proportion)", 0.02, 0.20, 0.08, step=0.01)

    if len(chosen_features) < 2:
        st.warning("Please select at least 2 physical features to train Isolation Forest.")
    else:
        iso_res = MicrogravityMLEngine.run_isolation_forest(
            df=df,
            feature_cols=chosen_features,
            contamination=contamination
        )

        if not iso_res.get("trained"):
            st.error(f"Cannot train model: {iso_res.get('reason')}")
        else:
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Training Samples</div>
                        <div style="color: #00d2ff; font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono';">{iso_res['training_samples']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_m2:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Anomalies Flagged</div>
                        <div style="color: #ff6b4a; font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono';">{iso_res['anomaly_count']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_m3:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Anomaly Ratio</div>
                        <div style="color: #f7b731; font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono';">{iso_res['anomaly_percentage']}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_m4:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Mean Score</div>
                        <div style="color: #20bf6b; font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono';">{iso_res['mean_anomaly_score']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")
            res_df = iso_res["result_dataframe"]

            # Scatter projection
            col_px, col_py = st.columns(2)
            with col_px:
                px_var = st.selectbox("X-Axis Projection", options=chosen_features, index=0)
            with col_py:
                py_var = st.selectbox("Y-Axis Projection", options=chosen_features, index=min(1, len(chosen_features)-1))

            fig_anom = create_anomaly_scatter(
                res_df,
                x_col=px_var,
                y_col=py_var,
                title=f"Isolation Forest Multi-Dimensional Anomaly Projection: {py_var} vs. {px_var}"
            )
            st.plotly_chart(fig_anom, use_container_width=True)

            st.markdown("#### 🚩 Flagged Outlier Observations Details:")
            flagged = iso_res.get("flagged_samples", [])
            if flagged:
                flat_flagged = []
                for item in flagged:
                    row = {
                        "Identifier": item["identifier"],
                        "Anomaly Score": item["anomaly_score"],
                        "Fuel Material": item["fuel_material"]
                    }
                    row.update(item["values"])
                    flat_flagged.append(row)
                st.dataframe(pd.DataFrame(flat_flagged), use_container_width=True)
            else:
                st.info("No anomalies detected at this contamination threshold.")

# Tab 2: Univariate IQR Profiler
with method_tabs[1]:
    st.markdown("### 📏 Univariate Tukey IQR Outlier Profiler")
    sel_col = st.selectbox("Select Target Variable", options=num_cols, key="iqr_col_select")
    mult = st.slider("IQR Multiplier (Fence distance)", 1.0, 3.0, 1.5, step=0.25)

    iqr_res = StatisticalAnomalyDetector.detect_univariate_outliers(df, col_name=sel_col, iqr_multiplier=mult)

    if not iqr_res.get("valid"):
        st.warning(iqr_res.get("reason"))
    else:
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 15px;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap; font-family: 'JetBrains Mono'; font-size: 0.85rem;">
                    <div><span style="color:#64748b;">IQR:</span> {iqr_res['iqr']}</div>
                    <div><span style="color:#64748b;">Q25 / Q75:</span> [{iqr_res['q25']}, {iqr_res['q75']}]</div>
                    <div><span style="color:#64748b;">Fences:</span> [{iqr_res['lower_bound']}, {iqr_res['upper_bound']}]</div>
                    <div><span style="color:#64748b;">Outliers Flagged:</span> <strong style="color:#ff6b4a;">{iqr_res['outlier_count']}</strong> ({iqr_res['outlier_pct']}%)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        outliers = iqr_res.get("outliers", [])
        if outliers:
            st.dataframe(pd.DataFrame(outliers), use_container_width=True)
        else:
            st.success("No univariate outliers detected outside the specified IQR fences.")
