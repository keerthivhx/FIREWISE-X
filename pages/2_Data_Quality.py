"""
Page 2: Data Quality Assessment
Comprehensive scientific health check, column profiling, physical bounds validation, and cleaning audit.
"""

import streamlit as st
import pandas as pd

from components.styles import apply_custom_theme
from components.source_status import render_source_status_banner
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile

st.set_page_config(page_title="Data Quality | FIREWISE-X", page_icon="🛡️", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("🛡️ Scientific Data Quality & Validation")
st.markdown("Audit data integrity, completeness, physical bounds compliance, and reproducible transformations.")

if "active_df" not in st.session_state or st.session_state.active_df.empty:
    st.warning("No active dataset loaded. Please navigate to the main Dashboard first.")
    st.stop()

df = st.session_state.active_df
meta = st.session_state.active_meta
quality = st.session_state.active_quality
clean_log = st.session_state.get("clean_log", [])

render_source_status_banner(meta)

# Top Health Score Metric Banner with Glassmorphic Cards
health_score = quality.get("health_score", 0)
score_color = "#20bf6b" if health_score >= 80 else "#f7b731" if health_score >= 60 else "#eb3b5a"
score_status = "EXCELLENT" if health_score >= 80 else "MODERATE" if health_score >= 60 else "DEGRADED"

q_col1, q_col2, q_col3, q_col4 = st.columns(4)

with q_col1:
    st.markdown(
        f"""
        <div class="glass-card" style="border-top: 3px solid {score_color};">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Composite Health Score</div>
            <div style="color: {score_color}; font-size: 1.85rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">
                {health_score:.1f} <span style="font-size: 0.95rem; color: #64748b;">/ 100</span>
            </div>
            <div style="color: {score_color}; font-size: 0.75rem; font-weight: 600;">STATUS: {score_status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with q_col2:
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Matrix Completeness</div>
            <div style="color: #00d2ff; font-size: 1.85rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">
                {quality.get('overall_completeness_pct', 0)}%
            </div>
            <div style="color: #64748b; font-size: 0.75rem;">Total Null Cells: {quality.get('total_missing_cells', 0):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with q_col3:
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Duplicate Records</div>
            <div style="color: #20bf6b; font-size: 1.85rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">
                {quality.get('duplicate_count', 0)}
            </div>
            <div style="color: #64748b; font-size: 0.75rem;">100% Unique observations</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with q_col4:
    viol_total = quality.get('physical_violations_total', 0)
    viol_color = "#20bf6b" if viol_total == 0 else "#f7b731"
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Physical Bounds Violations</div>
            <div style="color: {viol_color}; font-size: 1.85rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">
                {viol_total}
            </div>
            <div style="color: #64748b; font-size: 0.75rem;">Thermodynamic boundary checks</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# Detected Quality Notices
st.markdown("### ⚠️ Validation Audit Findings")
issues = quality.get("issues", [])
if issues:
    for issue in issues:
        st.markdown(
            f"""
            <div style="background: rgba(247, 183, 49, 0.08); border: 1px solid rgba(247, 183, 49, 0.3); 
                        border-left: 4px solid #f7b731; border-radius: 6px; padding: 10px 16px; margin-bottom: 8px; font-size: 0.9rem; color: #cbd5e1;">
                <strong style="color: #f7b731;">Notice:</strong> {issue}
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown(
        """
        <div style="background: rgba(32, 191, 107, 0.08); border: 1px solid rgba(32, 191, 107, 0.3); 
                    border-left: 4px solid #20bf6b; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px; font-size: 0.92rem; color: #20bf6b;">
            ✅ All evaluated attributes strictly conform to physical thermodynamic boundaries and scientific schema constraints.
        </div>
        """,
        unsafe_allow_html=True
    )

# Column-by-Column Scientific Profile Table
st.markdown("### 📋 Column Profiles & Physical Bounds Rules")
profiles = quality.get("column_profiles", {})

profile_rows = []
for col_name, prof in profiles.items():
    profile_rows.append({
        "Attribute": col_name,
        "Type": prof.get("inferred_type"),
        "Missing": f"{prof.get('missing_count')} ({prof.get('missing_pct')}%)",
        "Unique": prof.get("unique_values"),
        "Min": prof.get("min", "—"),
        "Mean": prof.get("mean", "—"),
        "Max": prof.get("max", "—"),
        "Physical Rule": prof.get("physical_rule", "Unbounded Generic"),
        "Flagged": prof.get("violations", 0)
    })

profile_table = pd.DataFrame(profile_rows)
st.dataframe(profile_table, use_container_width=True, height=360)

# Data Cleaning & Transformation Audit Log
st.markdown("### 🔄 Transparent Cleaning & Transformation Audit Trail")
st.markdown(
    """
    *In compliance with scientific reproducibility, all transformations performed during ingestion are logged below. 
    Raw measurements are preserved; physical bounds checks do not discard valid extreme readings.*
    """
)

if clean_log:
    for step_idx, step in enumerate(clean_log, 1):
        st.markdown(
            f"""
            <div style="background: rgba(14, 21, 45, 0.6); border: 1px solid rgba(0, 210, 255, 0.15); 
                        border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.88rem;">
                <span style="color: #00d2ff; font-weight: 700; font-family: 'JetBrains Mono'; margin-right: 8px;">STEP {step_idx:02d}:</span>
                <span style="color: #e2e8f0;">{step}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No modifications were required for this dataset.")
