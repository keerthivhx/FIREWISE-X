"""
Sidebar Navigation Component for FIREWISE-X
Ensures prominent, high-contrast, fully visible multi-page navigation across all screens.
"""

import streamlit as st

def render_sidebar_navigation(current_page: str = ""):
    """Renders prominent, styled native page links in the sidebar."""
    st.sidebar.markdown(
        """
        <div style="padding-top: 8px; margin-bottom: 8px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #00d2ff; letter-spacing: 1px; text-transform: uppercase;">
                📂 Mission Navigation
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.page_link("app.py", label="Dashboard", icon="🔥")
    st.sidebar.page_link("pages/1_Research_Explorer.py", label="1. Research Explorer", icon="🔍")
    st.sidebar.page_link("pages/2_Data_Quality.py", label="2. Data Quality", icon="🛡️")
    st.sidebar.page_link("pages/3_Scientific_Analysis.py", label="3. Scientific Analysis", icon="📈")
    st.sidebar.page_link("pages/4_Anomaly_Explorer.py", label="4. Anomaly Explorer", icon="⚡")
    st.sidebar.page_link("pages/5_Evidence_and_Insights.py", label="5. Evidence & Insights", icon="💡")
    st.sidebar.page_link("pages/6_About_and_Methodology.py", label="6. Methodology", icon="📚")
    st.sidebar.page_link("pages/7_Data_Import_and_Export.py", label="7. Import & Export", icon="💾")

    st.sidebar.write("---")
