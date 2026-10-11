"""
Page 5: Evidence and Insights
Synthesizes verifiable findings with supporting metrics, methodological lineage, citations, and uncertainty.
"""

import streamlit as st
import pandas as pd

from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile
from components.source_status import render_source_status_banner
from components.evidence_cards import render_evidence_cards
from src.insights.evidence import EvidenceInsightEngine

st.set_page_config(page_title="Evidence & Insights | FIREWISE-X", page_icon="💡", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("💡 Evidence-Based Scientific Insights")
st.markdown("Auditable scientific findings derived dynamically from the active microgravity combustion dataset.")

if "active_df" not in st.session_state or st.session_state.active_df.empty:
    st.warning("No active dataset loaded. Please navigate to the main Dashboard first.")
    st.stop()

df = st.session_state.active_df
meta = st.session_state.active_meta
findings = st.session_state.get("active_findings", [])

render_source_status_banner(meta)

# Regenerate findings if needed
if not findings:
    findings = EvidenceInsightEngine.generate_findings(df, meta)
    st.session_state.active_findings = findings

# Category filter pills
categories = ["All Categories"] + sorted(list(set(f.get("category", "General") for f in findings)))
selected_cat = st.selectbox("Filter Findings by Scientific Category", options=categories)

filtered_findings = findings
if selected_cat != "All Categories":
    filtered_findings = [f for f in findings if f.get("category") == selected_cat]

st.markdown(
    f"""
    <div style="margin: 12px 0 20px 0; font-size: 0.88rem; color: #94a3b8;">
        Displaying <strong style="color: #00d2ff;">{len(filtered_findings)}</strong> evidence findings 
        derived dynamically from {len(df)} active records in <strong>{meta.get('source_name', 'Active Dataset')}</strong>.
    </div>
    """,
    unsafe_allow_html=True
)

# Render structured evidence cards
render_evidence_cards(filtered_findings)
