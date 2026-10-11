"""
Source Status, Provenance & Mission Control Telemetry Component for FIREWISE-X
Displays authentic connection health, timestamps, record counts, and telemetry taxonomy.
"""

from typing import Dict, Any
from datetime import datetime, timezone
import streamlit as st

def render_source_status_banner(meta: Dict[str, Any]):
    """Renders the top status banner with connection health and data provenance."""
    source_name = meta.get("source_name", "Unspecified Scientific Source")
    source_url = meta.get("source_url", "#")
    status = meta.get("status", "Unknown")
    freshness = meta.get("freshness_type", "Standard")
    age = meta.get("data_age", "N/A")
    record_count = meta.get("record_count", 0)
    retrieval_time = meta.get("retrieval_time", "N/A")
    warning = meta.get("warning")
    error = meta.get("error")

    # Format timestamp nicely
    if retrieval_time and retrieval_time != "N/A":
        try:
            dt = datetime.fromisoformat(retrieval_time)
            ts_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            ts_str = str(retrieval_time)[:19]
    else:
        ts_str = "Not Available"

    # Status color coding
    if "Success" in status or "Fresh" in freshness:
        badge_bg = "rgba(32, 191, 107, 0.15)"
        badge_border = "#20bf6b"
        badge_text = "#20bf6b"
        pulse_html = '<span class="pulse-dot"></span>'
        status_label = "ONLINE SYNCHRONIZED"
    elif "Cached" in freshness or "Cached" in status:
        badge_bg = "rgba(247, 183, 49, 0.15)"
        badge_border = "#f7b731"
        badge_text = "#f7b731"
        pulse_html = '<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#f7b731; margin-right:6px;"></span>'
        status_label = "RESEARCH ARCHIVE CACHED"
    else:
        badge_bg = "rgba(235, 59, 90, 0.15)"
        badge_border = "#eb3b5a"
        badge_text = "#eb3b5a"
        pulse_html = '<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#eb3b5a; margin-right:6px;"></span>'
        status_label = "ENDPOINT CONNECTION ERROR"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(14, 21, 45, 0.95) 0%, rgba(18, 28, 60, 0.8) 100%); 
                    border: 1px solid rgba(0, 210, 255, 0.2); 
                    border-left: 4px solid #00d2ff; 
                    border-radius: 10px; 
                    padding: 16px 20px; 
                    margin-bottom: 22px; 
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_text}; 
                                 font-weight: 700; font-size: 0.72rem; padding: 4px 10px; border-radius: 20px; 
                                 letter-spacing: 0.6px; display: inline-flex; align-items: center;">
                        {pulse_html} {status_label}
                    </span>
                    <span style="color: #ffffff; font-size: 1.05rem; font-weight: 600;">{source_name}</span>
                    <a href="{source_url}" target="_blank" 
                       style="color: #00d2ff; text-decoration: none; font-size: 0.8rem; background: rgba(0, 210, 255, 0.08); 
                              padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(0, 210, 255, 0.2);">
                        Official Source ↗
                    </a>
                </div>
                <div style="display: flex; gap: 20px; color: #94a3b8; font-size: 0.82rem; font-family: 'JetBrains Mono', Consolas, monospace;">
                    <div><span style="color: #64748b;">RECORDS:</span> <span style="color: #00d2ff; font-weight: 700;">{record_count:,}</span></div>
                    <div><span style="color: #64748b;">STATE:</span> <span style="color: #e2e8f0;">{freshness}</span></div>
                    <div><span style="color: #64748b;">TIMESTAMP:</span> <span style="color: #e2e8f0;">{ts_str}</span></div>
                    <div><span style="color: #64748b;">AGE:</span> <span style="color: #e2e8f0;">{age}</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if warning:
        st.warning(f"⚠️ {warning}")
    if error:
        st.error(f"❌ {error}")


def render_telemetry_clarification():
    """Renders the required scientific clarification of telemetry terms."""
    with st.expander("🛰️ Mission Telemetry & Data Freshness Protocol Reference", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                <div style="background: rgba(14, 21, 45, 0.5); border: 1px solid rgba(0, 210, 255, 0.12); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                    <strong style="color: #00d2ff;">1. Online Retrieval (Active)</strong>
                    <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px; margin-bottom: 0;">
                        Direct HTTPS API requests querying live NASA STI/NTRS endpoints and authentic spaceflight repositories.
                    </p>
                </div>
                <div style="background: rgba(14, 21, 45, 0.5); border: 1px solid rgba(0, 210, 255, 0.12); border-radius: 8px; padding: 12px 16px;">
                    <strong style="color: #20bf6b;">2. Periodic Cache Refresh</strong>
                    <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px; margin-bottom: 0;">
                        Scheduled or manual synchronization with automated fallback to preserve validated research archives.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                """
                <div style="background: rgba(14, 21, 45, 0.5); border: 1px solid rgba(0, 210, 255, 0.12); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                    <strong style="color: #f7b731;">3. Reactive Scientific Analysis</strong>
                    <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px; margin-bottom: 0;">
                        Instantaneous recalculation of thermodynamic statistics, correlations, and ML models upon filter changes.
                    </p>
                </div>
                <div style="background: rgba(14, 21, 45, 0.5); border: 1px solid rgba(0, 210, 255, 0.12); border-radius: 8px; padding: 12px 16px;">
                    <strong style="color: #ff6b4a;">4. Live Telemetry Boundary</strong>
                    <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px; margin-bottom: 0;">
                        Continuous orbital streams are restricted to Mission Control (MCC-H). FIREWISE-X analyzes completed, validated flight runs.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
