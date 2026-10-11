"""
Page 1: Research Explorer
Interactive browsing, multi-parameter filtering, and provenance inspection of retrieved records.
"""

import streamlit as st
import pandas as pd

from components.styles import apply_custom_theme
from components.source_status import render_source_status_banner
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile

st.set_page_config(page_title="Research Explorer | FIREWISE-X", page_icon="🔍", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("🔍 Research Explorer")
st.markdown("Browse, filter, and inspect verified microgravity combustion records and technical metadata.")

if "active_df" not in st.session_state or st.session_state.active_df.empty:
    st.warning("No active dataset loaded. Please navigate to the main Dashboard first.")
    st.stop()

df = st.session_state.active_df
meta = st.session_state.active_meta
connector = st.session_state.connectors.get(st.session_state.current_source_key)

render_source_status_banner(meta)

# Source Capabilities and Protocol Details
if connector:
    caps = connector.describe_capabilities()
    with st.expander("📖 Source Capabilities, Protocol & Licensing Reference", expanded=False):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown(f"**Facility / Source:** `{caps.get('name')}`")
            st.markdown(f"**Description:** {caps.get('description')}")
            st.markdown(f"**Access Rights:** <span style='color:#20bf6b;'>{caps.get('access_restrictions')}</span>", unsafe_allow_html=True)
        with c_p2:
            st.markdown(f"**Known Limitations:** *{caps.get('limitations')}*")
            st.markdown("**Recorded Measurement Fields:**")
            for k, v in list(caps.get("measurements", {}).items())[:4]:
                st.markdown(f"- `{k}`: {v}")

# Filter Controls Section
st.markdown("### 🎛️ Filter Records")
f_col1, f_col2, f_col3 = st.columns(3)

filtered_df = df.copy()

# Filter 1: Keyword search across text columns
with f_col1:
    search_query = st.text_input("🔍 Search Text Fields", placeholder="e.g. PMMA, Cygnus, extinction, GRC")
    if search_query:
        query = search_query.lower()
        text_cols = filtered_df.select_dtypes(include=["object"]).columns
        mask = filtered_df[text_cols].astype(str).apply(lambda s: s.str.lower().str.contains(query)).any(axis=1)
        filtered_df = filtered_df[mask]

# Filter 2: Category Filter if fuel_category or center exists
with f_col2:
    if "fuel_category" in df.columns:
        fuels = ["All Fuels"] + sorted(df["fuel_category"].dropna().unique().tolist())
        selected_fuel = st.selectbox("🧪 Fuel Category", options=fuels)
        if selected_fuel != "All Fuels":
            filtered_df = filtered_df[filtered_df["fuel_category"] == selected_fuel]
    elif "center" in df.columns:
        centers = ["All Centers"] + sorted(df["center"].dropna().unique().tolist())
        selected_center = st.selectbox("🏛️ NASA Center", options=centers)
        if selected_center != "All Centers":
            filtered_df = filtered_df[filtered_df["center"] == selected_center]
    else:
        st.write("")

# Filter 3: Numeric range slider if O2% exists
with f_col3:
    if "initial_o2_pct" in df.columns:
        s_num = pd.to_numeric(df["initial_o2_pct"], errors="coerce").dropna()
        if not s_num.empty and s_num.min() < s_num.max():
            o2_range = st.slider(
                "💨 Baseline O₂ Concentration (% vol)",
                float(s_num.min()), float(s_num.max()),
                (float(s_num.min()), float(s_num.max())),
                step=0.1
            )
            filtered_df = filtered_df[
                (pd.to_numeric(filtered_df["initial_o2_pct"], errors="coerce") >= o2_range[0]) &
                (pd.to_numeric(filtered_df["initial_o2_pct"], errors="coerce") <= o2_range[1])
            ]
    else:
        st.write("")

st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
        <span style="font-size: 0.88rem; color: #94a3b8;">
            Showing <strong style="color: #00d2ff;">{len(filtered_df)}</strong> of {len(df)} records matching active criteria.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Interactive Records Table
st.dataframe(filtered_df, use_container_width=True, height=420)

# Record Detail Inspector
st.markdown("### 🔬 Inspect Single Record Details")
id_col = "test_id" if "test_id" in filtered_df.columns else "citation_id" if "citation_id" in filtered_df.columns else filtered_df.columns[0]
valid_ids = filtered_df[id_col].dropna().astype(str).unique()

if len(valid_ids) > 0:
    selected_id = st.selectbox("Select Record Identifier to Inspect", options=valid_ids)
    record_row = filtered_df[filtered_df[id_col].astype(str) == selected_id].iloc[0]

    with st.container():
        st.markdown(
            f"""
            <div style="background: rgba(14, 21, 45, 0.85); border: 1px solid rgba(0, 210, 255, 0.25); 
                        border-left: 4px solid #00d2ff; border-radius: 8px; padding: 16px 20px; margin-top: 10px; margin-bottom: 15px;">
                <h4 style="color: #00d2ff; margin: 0 0 4px 0;">Flight Record: {selected_id}</h4>
                <div style="color: #94a3b8; font-size: 0.82rem;">Archival Physical Parameter Breakdown</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        row_dict = record_row.to_dict()
        tab_gas, tab_cond, tab_raw = st.tabs(["🔥 Combustion Gas Kinetics", "⚙️ Test Conditions & Flow", "📋 All Raw Attributes"])

        with tab_gas:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Initial O₂", f"{row_dict.get('initial_o2_pct', '—')}%")
            c2.metric("Final O₂", f"{row_dict.get('final_o2_pct', '—')}%")
            c3.metric("Final CO₂", f"{row_dict.get('final_co2_pct', '—')}%")
            c4.metric("Final CO", f"{row_dict.get('final_co_ppm', '—')} ppm")

        with tab_cond:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Fuel", f"{row_dict.get('fuel_category', row_dict.get('fuel_material', '—'))}")
            c2.metric("Fan Speed", f"{row_dict.get('fan_display', '—')}")
            c3.metric("Flow Restrictor", f"{row_dict.get('flow_restrictor', '—')}")
            c4.metric("Camera Frames", f"{row_dict.get('total_frames', '—')}")

        with tab_raw:
            st.json(row_dict)
