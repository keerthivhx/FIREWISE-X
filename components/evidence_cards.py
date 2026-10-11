"""
Evidence Cards UI Component for FIREWISE-X
Renders evidence-based scientific findings with supporting metrics, citations, and limitations.
"""

from typing import Dict, Any, List
import streamlit as st

CATEGORY_COLORS = {
    "Life Support": {"border": "#ff6b4a", "bg": "rgba(255, 107, 74, 0.12)", "text": "#ff6b4a"},
    "Spacecraft Life Support Safety": {"border": "#ff6b4a", "bg": "rgba(255, 107, 74, 0.12)", "text": "#ff6b4a"},
    "Combustion Kinetics": {"border": "#00d2ff", "bg": "rgba(0, 210, 255, 0.12)", "text": "#00d2ff"},
    "Material Flammability Standards": {"border": "#f7b731", "bg": "rgba(247, 183, 49, 0.12)", "text": "#f7b731"},
    "Dataset Architecture & Evidence Base": {"border": "#20bf6b", "bg": "rgba(32, 191, 107, 0.12)", "text": "#20bf6b"},
    "Literature & Technical Investigation Scope": {"border": "#a55eea", "bg": "rgba(165, 94, 234, 0.12)", "text": "#a55eea"},
}

def render_evidence_cards(findings: List[Dict[str, Any]]):
    """Renders structured cards for each evidence-backed insight with category styling."""
    if not findings:
        st.info("No evidence findings generated yet for the current dataset.")
        return

    for idx, item in enumerate(findings, 1):
        category = item.get("category", "General")
        style = CATEGORY_COLORS.get(category, {"border": "#00d2ff", "bg": "rgba(0, 210, 255, 0.12)", "text": "#00d2ff"})

        with st.container():
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(14, 21, 45, 0.85) 0%, rgba(18, 28, 60, 0.75) 100%); 
                            border: 1px solid rgba(0, 210, 255, 0.18); 
                            border-left: 5px solid {style['border']}; 
                            border-radius: 10px; 
                            padding: 20px 24px; 
                            margin-bottom: 22px;
                            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                        <span style="font-size: 1.18rem; font-weight: 700; color: #ffffff;">
                            Finding #{idx}: {item.get('title')}
                        </span>
                        <span style="background: {style['bg']}; color: {style['text']}; font-size: 0.75rem; 
                                     font-weight: 700; padding: 4px 10px; border-radius: 20px; 
                                     border: 1px solid {style['border']}; letter-spacing: 0.5px; text-transform: uppercase;">
                            {category}
                        </span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.6; margin-bottom: 16px;">
                        {item.get('finding')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Metrics row
            metrics = item.get("evidence_metrics", {})
            if metrics:
                metric_items = list(metrics.items())
                cols = st.columns(min(len(metric_items), 4))
                for c_idx, (k, v) in enumerate(metric_items[:4]):
                    cols[c_idx].metric(label=k, value=str(v))

            # Methodology, citation, and limitations in expandable tray
            with st.expander(f"🔍 Scientific Lineage, Citation & Uncertainty for Finding #{idx}", expanded=False):
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    st.markdown(f"**Analytical Method:** `{item.get('methodology')}`")
                    st.markdown(f"**Assumptions:** *{item.get('assumptions')}*")
                with c_m2:
                    st.markdown(f"**Source Reference:** {item.get('source_citation')}")
                    st.markdown(f"**Known Limitations:** <span style='color: #ff6b4a;'>{item.get('limitations')}</span>", unsafe_allow_html=True)

            st.write("")
