"""
Page 7: Data Import and Export
Facilitates user-uploaded dataset validation, analysis ingestion, and scientific report exports.
"""

import io
import streamlit as st
import pandas as pd
import json

from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile
from components.source_status import render_source_status_banner
from src.validation.quality import DataQualityEngine
from src.processing.cleaning import ScientificDataCleaner
from src.insights.evidence import EvidenceInsightEngine
from src.reporting.exports import ReportGenerator
from src.ml.models import MicrogravityMLEngine

st.set_page_config(page_title="Import & Export | FIREWISE-X", page_icon="💾", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("💾 Data Import & Scientific Report Export")
st.markdown("Import external flight or laboratory combustion files and generate exportable research dossiers.")

tab_export, tab_import = st.tabs(["📤 Export Research Report & Data", "📥 Import External Dataset"])

# Tab 1: Export Current Analysis
with tab_export:
    st.markdown("### 📄 Export Active Analysis Dossier")

    if "active_df" not in st.session_state or st.session_state.active_df.empty:
        st.warning("No active dataset loaded to export.")
    else:
        df = st.session_state.active_df
        meta = st.session_state.active_meta
        quality = st.session_state.active_quality
        findings = st.session_state.get("active_findings", [])

        # Run ML summary for report if possible
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        ml_summary = {"trained": False, "reason": "Insufficient features"}
        if len(num_cols) >= 2:
            ml_summary = MicrogravityMLEngine.run_isolation_forest(df)

        report_md = ReportGenerator.generate_markdown_report(
            df=df,
            meta=meta,
            quality=quality,
            findings=findings,
            ml_results=ml_summary
        )

        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 20px;">
                <div style="font-size: 0.82rem; color: #94a3b8; text-transform: uppercase;">Export Target</div>
                <div style="font-size: 1.15rem; color: #ffffff; font-weight: 600; margin: 4px 0;">{meta.get('source_name', 'Active Dataset')}</div>
                <div style="font-size: 0.8rem; color: #64748b;">Includes: {len(df):,} records, Health Score {quality.get('health_score', 0):.1f}/100, {len(findings)} findings</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label="📥 Download Scientific Report (Markdown .md)",
            data=report_md,
            file_name=f"firewise_x_scientific_report_{meta.get('source_name', 'export').lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Active Records (CSV)",
                data=csv_data,
                file_name="firewise_x_records.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_d2:
            json_export = {
                "metadata": meta,
                "quality": quality,
                "findings": findings,
                "records": df.to_dict(orient="records")
            }
            st.download_button(
                label="📥 Download Structured Dossier (JSON)",
                data=json.dumps(json_export, indent=2),
                file_name="firewise_x_dossier.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("#### Preview Generated Scientific Dossier:")
        st.text_area("Markdown Report Text", value=report_md, height=350)

# Tab 2: Import Custom Dataset
with tab_import:
    st.markdown("### 📥 Ingest Custom Experimental Dataset")
    st.markdown(
        """
        Upload your own experimental CSV or JSON dataset (e.g. drop tower tests, parabolic flight logs, 
        or combustion kinetics measurements). Uploaded files pass through the identical validation and 
        scientific analysis pipeline as NASA online records.
        """
    )

    uploaded_file = st.file_uploader("Select Tabular File (.csv or .json)", type=["csv", "json"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            else:
                df_upload = pd.read_json(uploaded_file)

            st.success(f"Successfully parsed {len(df_upload)} records and {len(df_upload.columns)} columns.")

            # Immediate validation preview
            upload_quality = DataQualityEngine.evaluate(df_upload)
            st.markdown(
                f"""
                <div class="glass-card" style="margin: 15px 0;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Uploaded File Validation</div>
                    <div style="font-size: 1.4rem; color: #20bf6b; font-weight: 700; font-family: 'JetBrains Mono'; margin: 4px 0;">
                        Health Index: {upload_quality['health_score']}/100
                    </div>
                    <div style="font-size: 0.85rem; color: #cbd5e1;">Completeness: {upload_quality['overall_completeness_pct']}% | Duplicates: {upload_quality['duplicate_count']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("🚀 Load Uploaded Dataset as Active Analysis Dataset", use_container_width=True):
                df_clean, clean_log = ScientificDataCleaner.clean(df_upload)
                custom_meta = {
                    "source_name": f"User Upload ({uploaded_file.name})",
                    "source_url": "Local File Upload",
                    "retrieval_time": pd.Timestamp.now().isoformat(),
                    "record_count": len(df_upload),
                    "is_cached": False,
                    "freshness_type": "User Uploaded Dataset",
                    "status": "Validated Local Import"
                }

                st.session_state.raw_df = df_upload
                st.session_state.active_df = df_clean
                st.session_state.active_meta = custom_meta
                st.session_state.clean_log = clean_log
                st.session_state.active_quality = upload_quality
                st.session_state.active_findings = EvidenceInsightEngine.generate_findings(df_clean, custom_meta)
                st.session_state.current_source_key = "user_upload"

                st.success("Custom dataset activated! You can now explore it across all analytical pages.")
                st.rerun()

        except Exception as e:
            st.error(f"Error parsing uploaded file: {e}")
