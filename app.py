"""
FIREWISE-X: AI-Powered Fire Safety Insights from Microgravity Combustion Data
NASA Space Apps Challenge 2026 • Flame in Freefall
Main Application Entrypoint & Mission Research Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="FIREWISE-X | Spacecraft Fire Safety Research",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile
from components.source_status import render_source_status_banner, render_telemetry_clarification
from components.charts import create_scatter_plot, create_histogram, create_box_plot
from src.ingestion.nasa_bass import NASABass2Connector
from src.ingestion.nasa_saffire import NASASaffireConnector
from src.ingestion.nasa_sofie import NASASofieConnector
from src.ingestion.nasa_ntrs import NASANtrsConnector
from src.validation.quality import DataQualityEngine
from src.processing.cleaning import ScientificDataCleaner
from src.analysis.descriptive import DescriptiveAnalyzer
from src.insights.evidence import EvidenceInsightEngine
from src.ml.models import MicrogravityMLEngine

# Inject custom space science styling
apply_custom_theme()

# Enforce Mission Control Authentication
check_authentication()

def init_session_state():
    """Initializes global dataset state in Streamlit session."""
    if "connectors" not in st.session_state:
        st.session_state.connectors = {
            "bass2": NASABass2Connector(),
            "saffire": NASASaffireConnector(),
            "sofie": NASASofieConnector(),
            "ntrs": NASANtrsConnector(query="microgravity combustion flame spread")
        }

    if "current_source_key" not in st.session_state:
        st.session_state.current_source_key = "bass2"

    if "active_df" not in st.session_state:
        load_dataset(st.session_state.current_source_key, force_refresh=False)

def load_dataset(source_key: str, force_refresh: bool = False):
    """Loads and processes dataset from chosen source connector."""
    connector = st.session_state.connectors.get(source_key)
    if not connector:
        return

    with st.spinner(f"Synchronizing research records from {connector.name}..."):
        df_raw, meta = connector.fetch_data(force_refresh=force_refresh)

    if not df_raw.empty:
        df_clean, clean_log = ScientificDataCleaner.clean(df_raw)
        quality = DataQualityEngine.evaluate(df_clean)
        findings = EvidenceInsightEngine.generate_findings(df_clean, meta)

        st.session_state.raw_df = df_raw
        st.session_state.active_df = df_clean
        st.session_state.active_meta = meta
        st.session_state.clean_log = clean_log
        st.session_state.active_quality = quality
        st.session_state.active_findings = findings
        st.session_state.current_source_key = source_key
    else:
        st.session_state.raw_df = pd.DataFrame()
        st.session_state.active_df = pd.DataFrame()
        st.session_state.active_meta = meta
        st.session_state.clean_log = []
        st.session_state.active_quality = DataQualityEngine.evaluate(pd.DataFrame())
        st.session_state.active_findings = []
        st.session_state.current_source_key = source_key

init_session_state()

# Sidebar: Mission Control Branding & Controls
render_user_profile()

st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 6px 0 16px 0;">
        <div style="font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px; 
                    background: linear-gradient(90deg, #00d2ff 0%, #ff6b4a 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            FIREWISE-X
        </div>
        <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">
            NASA Space Apps 2026
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

source_options = {
    "bass2": "1. NASA ISS BASS-II (Flight Experiments)",
    "saffire": "2. NASA Saffire (Spacecraft Fire Records)",
    "sofie": "3. NASA SoFIE (ISS Combustion Rack)",
    "ntrs": "4. NASA NTRS (Live Research Query)"
}

st.sidebar.markdown("### 🛰️ **Active Flight Source**")
selected_key = st.sidebar.selectbox(
    "Select Source",
    options=list(source_options.keys()),
    format_func=lambda k: source_options[k],
    index=list(source_options.keys()).index(st.session_state.current_source_key),
    label_visibility="collapsed"
)

if selected_key != st.session_state.current_source_key:
    load_dataset(selected_key, force_refresh=False)
    st.rerun()

if st.sidebar.button("🔄 Force Online Refresh", use_container_width=True):
    load_dataset(st.session_state.current_source_key, force_refresh=True)
    st.rerun()

render_sidebar_navigation()

st.sidebar.markdown(
    """
    <div style="font-size: 0.75rem; color: #64748b; line-height: 1.4; padding: 4px 6px;">
        <strong style="color: #94a3b8;">STRICT INTEGRITY POLICY:</strong><br>
        100% computed from verified online NASA datasets. No mock telemetry or fabricated findings.
    </div>
    """,
    unsafe_allow_html=True
)

# Main Hero Banner
st.markdown(
    """
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                <span style="background: rgba(0, 210, 255, 0.15); color: #00d2ff; font-weight: 700; font-size: 0.72rem; 
                             padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(0, 210, 255, 0.3); letter-spacing: 0.6px;">
                    CHALLENGE: FLAME IN FREEFALL
                </span>
                <h1 style="color: #ffffff; font-size: 2.2rem; font-weight: 800; margin: 10px 0 6px 0; letter-spacing: -0.5px;">
                    FIREWISE-X
                </h1>
                <p style="color: #94a3b8; font-size: 1.05rem; margin-bottom: 0; max-width: 820px; line-height: 1.5;">
                    Translating empirical NASA microgravity combustion datasets into actionable fire safety insights.
                    Without buoyant convection in orbit, flames behave in spherical, slow-diffusing regimes with stealth smoldering hazards.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="background: rgba(14, 21, 45, 0.8); border: 1px solid rgba(0, 210, 255, 0.2); 
                            border-radius: 8px; padding: 10px 16px; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.8rem;">
                    <div style="color: #64748b;">MISSION PLATFORM</div>
                    <div style="color: #00d2ff; font-weight: 700;">NASA ISS & CYGNUS ARCHIVES</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

df = st.session_state.get("active_df", pd.DataFrame())
meta = st.session_state.get("active_meta", {})
quality = st.session_state.get("active_quality", {})

# Provenance Status Banner
render_source_status_banner(meta)
render_telemetry_clarification()

if df.empty:
    st.error("No records available for the active source. Please check internet connection or select a different source.")
    st.stop()

# Key Performance Indicators (Glassmorphic Cards)
st.markdown("### 📊 Active Scientific Parameters")
stats = DescriptiveAnalyzer.analyze(df)

kpi_cols = st.columns(5)

with kpi_cols[0]:
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Flight Records</div>
            <div style="color: #00d2ff; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{len(df):,}</div>
            <div style="color: #64748b; font-size: 0.75rem;">Verified observations</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_cols[1]:
    h_score = quality.get('health_score', 0)
    h_color = "#20bf6b" if h_score >= 80 else "#f7b731" if h_score >= 60 else "#eb3b5a"
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Data Health Index</div>
            <div style="color: {h_color}; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{h_score:.1f}<span style="font-size: 1rem; color: #64748b;">/100</span></div>
            <div style="color: #64748b; font-size: 0.75rem;">Completeness: {quality.get('overall_completeness_pct', 0)}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if "initial_o2_pct" in df.columns and "final_o2_pct" in df.columns:
    s_o2 = pd.to_numeric(df["initial_o2_pct"], errors="coerce").dropna()
    with kpi_cols[2]:
        val_str = f"{s_o2.mean():.1f}%" if not s_o2.empty else "N/A"
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Mean Baseline O₂</div>
                <div style="color: #00d2ff; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{val_str}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Range: {s_o2.min():.1f}% - {s_o2.max():.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi_cols[3]:
        if "delta_co_ppm" in df.columns:
            s_co = pd.to_numeric(df["delta_co_ppm"], errors="coerce").dropna()
            co_max = f"{s_co.max():.0f} ppm" if not s_co.empty else "N/A"
        elif "final_co_ppm" in df.columns:
            s_co = pd.to_numeric(df["final_co_ppm"], errors="coerce").dropna()
            co_max = f"{s_co.max():.0f} ppm" if not s_co.empty else "N/A"
        else:
            co_max = "N/A"
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Peak Toxic CO</div>
                <div style="color: #ff6b4a; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{co_max}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Toxic product build-up</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi_cols[4]:
        fuel_count = df['fuel_category'].nunique() if 'fuel_category' in df.columns else len(df.columns)
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Fuel Classes</div>
                <div style="color: #f7b731; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{fuel_count}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Solid polymer variants</div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    with kpi_cols[2]:
        centers = df["center"].dropna().nunique() if "center" in df.columns else "N/A"
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">NASA Centers</div>
                <div style="color: #00d2ff; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{centers}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Research facilities</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi_cols[3]:
        saffire_hits = df.get("is_saffire", pd.Series(dtype=bool)).sum() if "is_saffire" in df.columns else 0
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Saffire Records</div>
                <div style="color: #ff6b4a; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{saffire_hits}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Large-scale Cygnus fires</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi_cols[4]:
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">Dimensions</div>
                <div style="color: #20bf6b; font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">{len(df.columns)}</div>
                <div style="color: #64748b; font-size: 0.75rem;">Attributes cataloged</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# Main Dashboard Interactive Visualizations
st.markdown("### 📈 Core Empirical Relationships")

if "fan_display" in df.columns and "final_co_ppm" in df.columns:
    c_left, c_right = st.columns([13, 9])
    with c_left:
        fig_scatter = create_scatter_plot(
            df,
            x_col="fan_display",
            y_col="final_co_ppm",
            color_col="fuel_category" if "fuel_category" in df.columns else None,
            hover_name="test_id" if "test_id" in df.columns else None,
            title="Forced Flow Speed (Fan Display) vs. Toxic Carbon Monoxide Generation",
            add_trendline=True
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with c_right:
        fig_box = create_box_plot(
            df,
            x_col="fuel_category" if "fuel_category" in df.columns else "flow_restrictor",
            y_col="final_co_ppm",
            title="CO Emissions Distribution Across Fuel Types"
        )
        st.plotly_chart(fig_box, use_container_width=True)

elif "initial_o2_pct" in df.columns:
    c_left, c_right = st.columns([1, 1])
    with c_left:
        fig_hist = create_histogram(df, col="initial_o2_pct", title="Ambient Oxygen Concentration (% vol) Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)
    with c_right:
        if "final_o2_pct" in df.columns:
            fig_hist2 = create_histogram(df, col="final_o2_pct", title="Final Post-Burn Oxygen Concentration (% vol)")
            st.plotly_chart(fig_hist2, use_container_width=True)

else:
    if "center" in df.columns:
        counts = df["center"].value_counts().reset_index()
        counts.columns = ["center", "count"]
        fig_bar = create_scatter_plot(counts, x_col="center", y_col="count", title="Publications by NASA Research Center")
        st.plotly_chart(fig_bar, use_container_width=True)

# Dataset Preview & Direct Navigation Launchpad
st.markdown("### 📋 Active Dataset Record Stream")
st.dataframe(df.head(10), use_container_width=True)

st.write("")
st.markdown("### 🚀 Module Navigation Launchpad")
l_col1, l_col2, l_col3, l_col4 = st.columns(4)
with l_col1:
    st.page_link("pages/1_Research_Explorer.py", label="1. Research Explorer", icon="🔍")
    st.page_link("pages/2_Data_Quality.py", label="2. Data Quality", icon="🛡️")
with l_col2:
    st.page_link("pages/3_Scientific_Analysis.py", label="3. Scientific Analysis", icon="📈")
    st.page_link("pages/4_Anomaly_Explorer.py", label="4. Anomaly Explorer", icon="⚡")
with l_col3:
    st.page_link("pages/5_Evidence_and_Insights.py", label="5. Evidence & Insights", icon="💡")
    st.page_link("pages/6_About_and_Methodology.py", label="6. Methodology", icon="📚")
with l_col4:
    st.page_link("pages/7_Data_Import_and_Export.py", label="7. Import & Export", icon="💾")
    st.page_link("app.py", label="Back to Top / Dashboard", icon="🔥")
