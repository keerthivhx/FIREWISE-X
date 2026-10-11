"""
Page 6: About and Methodology
Comprehensive scientific reference, mathematical definitions, data lineages, and limitation boundaries.
"""

import streamlit as st
from components.styles import apply_custom_theme
from components.navigation import render_sidebar_navigation
from components.auth import check_authentication, render_user_profile

st.set_page_config(page_title="Methodology | FIREWISE-X", page_icon="📚", layout="wide")
apply_custom_theme()
check_authentication()
render_user_profile()
render_sidebar_navigation()

st.title("📚 Scientific Methodology & System Architecture")
st.markdown("Detailed reference for evaluators, judges, and researchers on the analytical foundations of FIREWISE-X.")

with st.expander("🚀 Project Overview & Space Apps 2026 Challenge Context", expanded=True):
    st.markdown(
        r"""
        **Challenge:** Flame in Freefall: AI-Powered Fire Safety Insights from Microgravity Combustion Data  
        **Team Project:** FIREWISE-X  
        **Tagline:** From Space Combustion Research to Evidence-Based Fire Safety Insights  

        ### Fundamental Physics of Microgravity Combustion:
        1. **Absence of Buoyant Convection:** On Earth, hot combustion gases are less dense than cold air and rise naturally, creating convective updrafts that supply fresh oxygen. In reduced gravity (\(g \approx 0\)), buoyancy ceases (\(Gr \to 0\)). Flames become spherical diffusion envelopes where oxygen transport relies entirely on slow molecular diffusion or forced ambient ventilation.
        2. **Slower Flame Spread & Stealth Smoldering:** Flames in spacecraft cabins can smolder quietly at low temperatures without visible smoke or flickering plumes, making conventional optical fire detectors less effective.
        3. **Toxic Gas Accumulation:** In the absence of upward buoyant draft, toxic combustion byproducts (Carbon Monoxide and soot) accumulate directly around the fuel surface, posing severe acute hazards to crew members if disturbed.
        """
    )

    st.markdown("#### Microgravity vs. Earth Combustion Transport Physics:")
    st.markdown(
        """
        ```mermaid
        flowchart LR
          subgraph Earth ["Terrestrial Gravity (1g)"]
            E1["Combustion Reaction"] --> E2["Density Gradient"]
            E2 --> E3["Buoyant Updraft (1-2 m/s)"]
            E3 --> E4["Teardrop Flame Plume"]
          end
          subgraph Space ["Microgravity (μg)"]
            S1["Combustion Reaction"] --> S2["Zero Buoyancy (Gr ≈ 0)"]
            S2 --> S3["Slow Molecular Diffusion"]
            S3 --> S4["Spherical Flame & Toxic CO Envelope"]
          end
        ```
        """
    )

with st.expander("🌐 1. Online Data Retrieval & Provenance Pipeline", expanded=True):
    st.markdown(
        """
        FIREWISE-X connects to official NASA and scientific repositories:
        - **NASA ISS BASS-II Flight Dataset:** Genuine flight telemetry and gas sampling records from 120+ microgravity solid fuel burning tests conducted in the Microgravity Science Glovebox on the ISS (PI: Prof. Subrata Bhattacharjee).
        - **NASA Saffire Records:** Technical flight findings from the Spacecraft Fire Safety Experiments conducted inside automated Cygnus cargo vehicles after departing the ISS.
        - **NASA SoFIE CIR Investigation Records:** Experiments performed in the Combustion Integrated Rack flow duct on the ISS.
        - **NASA Technical Reports Server (NTRS) API:** Live REST query access to peer-reviewed NASA STI papers and experiment documentation.
        
        **Provenance Guarantee:** Every dataset retains its source URL, ISO-8601 retrieval timestamp, freshness state, and caching metadata.
        """
    )

with st.expander("🛡️ 2. Scientific Data Quality Assessment Framework", expanded=False):
    st.markdown(
        r"""
        Data quality is evaluated across three primary pillars:
        
        $$\text{Health Score} = 0.50 \times \text{Completeness} + 0.30 \times \text{Uniqueness} + 0.20 \times \text{Physical Bounds Integrity}$$
        
        - **Completeness:** Ratio of valid non-null entries to total data matrix cells.
        - **Uniqueness:** 1 minus the duplicate row ratio.
        - **Physical Bounds Integrity:** Strict verification that physical variables lie within thermodynamically admissible intervals:
          - Oxygen concentration: \(0.0 \le [O_2] \le 100.0\%\) vol
          - Carbon dioxide concentration: \(0.0 \le [CO_2] \le 100.0\%\) vol
          - Carbon monoxide concentration: \([CO] \ge 0.0\) ppm
        """
    )

with st.expander("🤖 3. Machine Learning Formulation & Evaluation", expanded=False):
    st.markdown(
        r"""
        **Unsupervised Anomaly Isolation (Isolation Forest):**
        - **Objective:** Detect rare combustion operating regimes without relying on fabricated danger labels.
        - **Mechanism:** Builds an ensemble of recursive binary trees. Observations that require few random splits to isolate have short path lengths and low anomaly scores:
          $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
        - **Evaluation:** Evaluates decision score distributions, contamination thresholds, and feature standardizations via standard deviations.
        
        **Scientific Guardrails:**
        - Models are strictly refused when observations are fewer than 10 or numeric features fewer than 2.
        - Rule-based alerts are explicitly separated from trained machine learning.
        """
    )

with st.expander("⚠️ 4. Stated Limitations & Boundaries", expanded=False):
    st.markdown(
        """
        In strict adherence to scientific ethics:
        - **Not a Flight Safety Replacement:** FIREWISE-X is a scientific research and data exploration platform; it does not replace operational spacecraft Caution & Warning (C&W) emergency avionics.
        - **Archival Flight Datasets:** Real-time raw sensor telemetry feeds from the ISS are export-controlled (ITAR/EAR) and restricted to Mission Control Center (MCC-H). FIREWISE-X analyzes completed, validated flight datasets released through NASA PSI and NTRS.
        - **Offline Graceful Degradation:** If network connectivity is interrupted, the application transparently serves cached flight data clearly marked with historical timestamps.
        """
    )
