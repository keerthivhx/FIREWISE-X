# FIREWISE-X: AI-Powered Fire Safety Insights from Microgravity Combustion Data

> **From Space Combustion Research to Evidence-Based Fire Safety Insights**  
> *NASA Space Apps Challenge 2026 — Flame in Freefall*

---

## 1. Project Overview

**FIREWISE-X** is an online-data-driven scientific research platform designed to analyze empirical microgravity combustion data from NASA spaceflight experiments (including **ISS BASS-II**, **Saffire I–VI**, and **SoFIE**).

In terrestrial gravity, combustion is dominated by buoyancy-driven natural convection: hot gases rise, drawing fresh oxygen into the base of the flame. In reduced gravity (\(g \approx 0\)), buoyancy ceases, and flames become spherical, diffusion-limited, and prone to low-temperature smoldering in ventilation dead zones.

FIREWISE-X connects directly to verified NASA endpoints, audits data health, performs dynamic statistical and correlation analysis, applies explainable Isolation Forest anomaly detection, and synthesizes reproducible, evidence-based fire safety insights.

---

## 2. Key Objectives & Strict Integrity Policy

* **Strict No-Hardcoded-Data Policy:** Every visualization, metric, correlation matrix, and finding is calculated dynamically from the active online dataset. No synthetic measurements or static findings are hardcoded.
* **Online Data Ingestion Engine:** Connects directly to the **NASA Technical Reports Server (NTRS) REST API** and the **NASA PSI BASS-II flight repository**.
* **Scientific Data Quality:** Performs non-destructive audits evaluating completeness, duplicates, and thermodynamic boundary compliance without silently deleting extreme scientific readings.
* **Scientifically Justified ML:** Trains an unsupervised **Isolation Forest** on physical combustion parameters (oxygen consumption, fan speed, CO emissions) to isolate rare extinction or smoldering regimes with physical explanations.
* **Traceable Evidence Engine:** Formulates structured scientific findings linked directly to source citations, mathematical definitions, and stated uncertainties.

---

## 3. System Architecture

```
[ NASA Online Endpoints ]
  ├── NASA NTRS REST API (Live Search)
  ├── NASA ISS BASS-II Flight Repository
  ├── NASA Saffire Cygnus Flight Records
  └── NASA SoFIE CIR Investigation Records
              │
              ▼ (HTTPS / JSON / CSV)
[ Ingestion Layer (src/ingestion/) ]
  ├── BaseDataConnector (Provenance, Caching, Offline Fallback)
  └── Source-Specific Connectors (NTRS, BASS-II, Saffire, SoFIE)
              │
              ▼
[ Scientific Validation (src/validation/) ]
  ├── Completeness & Uniqueness Auditing
  └── Thermodynamic Physical Bounds Checking (O2, CO2, CO, Gain)
              │
              ▼
[ Processing & Analytics (src/processing/, src/analysis/) ]
  ├── Kinetics Derivation (ΔO2, ΔCO2, ΔCO, Flame Frames)
  ├── Descriptive Statistics & Quantiles
  ├── Pearson & Spearman Correlation Matrices
  └── Tukey IQR Outlier Profiling
              │
              ▼
[ Machine Learning Engine (src/ml/) ]
  ├── Pure Isolation Forest (100 Ensemble iTrees)
  └── Pure Lloyd's K-Means & Silhouette Validation
              │
              ▼
[ User Interface & Reporting (app.py, pages/, components/) ]
  ├── Interactive Deep-Space Dark Navy Dashboard
  ├── Multi-Parameter Filtering & Inspector
  └── Export Engine (CSV, JSON, Markdown Research Reports)
```

---

## 4. Technology Stack

* **Language:** Python 3.10+ (Verified on Python 3.14)
* **Web Framework:** Streamlit
* **Data Processing & Analytics:** Pandas, NumPy
* **Scientific Visualizations:** Plotly Express & Plotly Graph Objects
* **HTTP Client & Ingestion:** Requests, Urllib
* **Machine Learning:** Pure NumPy Isolation Forest & K-Means (100% resilient against platform DLL blocks)
* **Automated Testing:** Pytest

---

## 5. Project Directory Structure

```
FIREWISE-X/
├── app.py                         # Main Streamlit Entrypoint & Research Dashboard
├── pages/
│   ├── 1_Research_Explorer.py     # Filterable records browser & single-test inspector
│   ├── 2_Data_Quality.py          # Column profiling, physical bounds, & audit log
│   ├── 3_Scientific_Analysis.py   # Correlation heatmaps, distributions, bivariate plots
│   ├── 4_Anomaly_Explorer.py      # Isolation Forest & Tukey IQR anomaly profiler
│   ├── 5_Evidence_and_Insights.py # Structured evidence cards & scientific findings
│   ├── 6_About_and_Methodology.py # Theoretical foundations & challenge context
│   └── 7_Data_Import_and_Export.py# CSV/JSON import & Markdown report generation
├── components/
│   ├── charts.py                  # Standardized dark-navy Plotly figure factory
│   ├── source_status.py           # Top provenance & connection status banners
│   └── evidence_cards.py          # Structured cards for scientific insights
├── src/
│   ├── config.py                  # Endpoints, physical bounds, and UI theme colors
│   ├── ingestion/                 # Online connectors (BASS-II, NTRS, Saffire, SoFIE)
│   ├── validation/                # Quality assessment & boundary rules
│   ├── processing/                # Non-destructive cleaning & kinetics derivation
│   ├── analysis/                  # Descriptive, correlation, & outlier analyzers
│   ├── ml/                        # Pure NumPy Isolation Forest & K-Means
│   ├── insights/                  # Evidence generation with citations
│   └── reporting/                 # Structured scientific dossier export
├── tests/
│   ├── test_ingestion.py          # Caching, provenance, & generic HTTP tests
│   ├── test_validation.py         # Quality, completeness, & boundary tests
│   ├── test_analysis.py           # Descriptive stats, correlation, & ML guardrails
│   ├── test_refresh.py            # Cache refresh & network resilience tests
│   └── acceptance_live_test.py    # Mandatory online real-data verification suite
├── data/
│   └── cache/                     # Auto-managed data cache with ISO-8601 metadata
├── docs/
│   ├── DATA_SOURCES.md            # Verified scientific endpoints & access status
│   ├── METHODOLOGY.md             # Equations, derivations, & quality formulas
│   ├── LIMITATIONS.md             # Operational boundaries & ML limitations
│   └── DEMO_SCRIPT.md             # 3-minute presentation script for evaluators
├── requirements.txt               # Pinned dependencies
├── README.md                      # Complete documentation
├── .gitignore                     # Git ignore rules
└── .env.example                   # Environment configuration template
```

---

## 6. Installation & Execution Guide (Windows PowerShell)

Open **Windows PowerShell** in the project directory:

```powershell
# 1. Navigate to workspace
cd "c:\Users\keert\OneDrive\Desktop\Projects\Firewise"

# 2. (Optional) Create and activate virtual environment
py -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Run automated test suite
python -m pytest -v

# 5. Run live real-data acceptance verification
python -m tests.acceptance_live_test

# 6. Launch FIREWISE-X Application
python -m streamlit run app.py
```

The application will launch automatically in your default web browser at `http://localhost:8501`.

---

## 7. How to Use FIREWISE-X

### Switching Online Data Sources
1. Open the left sidebar in the application.
2. Under **"Active Online Data Source"**, select from:
   * **NASA ISS BASS-II:** 129 flight combustion tests aboard the ISS Microgravity Science Glovebox.
   * **NASA Saffire:** Flight records from large-scale Cygnus vehicle burn events.
   * **NASA SoFIE:** ISS Combustion Integrated Rack (CIR) experiments.
   * **NASA NTRS:** Live query search against the official NASA STI repository.
3. Click **"Force Online Refresh"** at any time to bypass cache and query the live endpoints.

### Inspecting Data Quality
* Open **Page 2: Data Quality** to inspect the overall Health Score, missing values, duplicates, and physical bounds checks.

### Running Multi-Dimensional Anomaly Isolation
* Open **Page 4: Anomaly Explorer**, select your desired physical combustion parameters, adjust the contamination fence, and inspect the flagged outliers along with their physical justifications.

### Importing Custom Datasets & Exporting Reports
* Open **Page 7: Data Import & Export** to drag-and-drop your own laboratory CSV/JSON files or download the comprehensive **Markdown Scientific Report**.

---

## 8. Known Limitations & Future Work

* **Telemetry Nature:** Flight records represent completed, verified archival datasets; real-time operational flight feeds from the ISS are export-controlled (ITAR/EAR).
* **Future Work:** Integration with NASA Open Science Data Repository (OSDR) multi-omics datasets to examine toxic byproduct inhalation exposure metrics.

---
*(c) 2026 FIREWISE-X Team — NASA Space Apps Challenge*
#   F I R E W I S E - X  
 