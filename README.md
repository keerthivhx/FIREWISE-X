# 🔥 FIREWISE-X

### AI-Powered Fire Safety Insights from Microgravity Combustion Data

**From Space Combustion Research to Evidence-Based Fire Safety Insights**

NASA Space Apps Challenge 2026 · *Flame in Freefall*

---

## 🌌 Project Overview

**FIREWISE-X** is a scientific data analysis platform designed to explore microgravity combustion research and investigate its potential implications for fire safety.

On Earth, gravity creates buoyancy-driven convection: hot gases rise while cooler gases move toward the flame. In microgravity, buoyancy-driven flow is greatly reduced, changing how heat, gases, and combustion products move around a flame. These conditions can affect flame shape, combustion behavior, and the persistence of smoldering.

FIREWISE-X aims to connect scientific research with data analysis through a web-based dashboard built using Python and Streamlit. It provides a framework for exploring combustion-related datasets, assessing data quality, examining statistical relationships, identifying unusual observations, and presenting findings with supporting evidence.

The project is designed to work with relevant NASA research resources, including studies associated with the Burning and Suppression of Solids (BASS), Spacecraft Fire Safety (Saffire), and the Solid Fuel Ignition and Extinction (SoFIE) investigation.

**Our goal:** make space-based combustion research easier to explore, analyze, and communicate while preserving scientific context and data provenance.

> **Scientific scope:** FIREWISE-X is a research and analysis prototype. Its outputs are exploratory insights, not certified fire-safety predictions or operational spacecraft safety recommendations.

---

## 🎯 Objectives

* **Explore scientific data:** Provide a structured interface for examining combustion research records and supported datasets.
* **Assess data quality:** Identify missing values, duplicate records, and potential physical-bound violations without silently discarding unusual observations.
* **Analyze relationships:** Calculate descriptive statistics, distributions, and correlations for suitable numerical variables.
* **Investigate anomalies:** Explore unusual observations using supported statistical and machine-learning methods.
* **Present traceable evidence:** Connect findings to available source information, definitions, assumptions, and limitations.
* **Support reproducibility:** Provide data export and research-report functionality where implemented.

---

## ✨ Key Features

### 1. Research Explorer

Browse available records, apply filters, and inspect individual observations where supported by the active dataset.

### 2. Data Quality Assessment

Examine dataset completeness, duplicate records, missing values, and configured validation checks.

### 3. Scientific Analysis

Explore numerical distributions, summary statistics, and relationships between variables using statistical analysis and visualizations.

### 4. Anomaly Explorer

Investigate unusual observations using supported anomaly-detection and outlier-analysis methods.

An anomaly is a record that differs from the patterns learned or statistical limits selected by the analysis. It is **not automatically a combustion failure or safety hazard**.

### 5. Evidence and Insights

Present analytical findings alongside available data provenance and supporting explanations. Conclusions should be interpreted in the context of the source data and analysis assumptions.

### 6. About and Methodology

Review the project's scientific motivation, analytical approach, assumptions, and limitations.

### 7. Data Import and Export

Work with supported custom datasets and export analysis results or research summaries using the available application features.

---

## 🏗️ System Architecture

FIREWISE-X is organized into modular layers for data ingestion, validation, processing, analysis, and presentation.

```text
                 SCIENTIFIC DATA SOURCES
                          |
             +------------+------------+
             |            |            |
          NASA NTRS    BASS-II      Saffire / SoFIE
             |            |            |
             +------------+------------+
                          |
                          v
                 DATA INGESTION
                    src/ingestion/
                          |
                          v
                 DATA VALIDATION
                  src/validation/
                          |
                          v
                 DATA PROCESSING
                  src/processing/
                          |
                          v
               SCIENTIFIC ANALYSIS
                   src/analysis/
                          |
                          v
                 ANALYTICAL MODELS
                      src/ml/
                          |
                          v
                 EVIDENCE GENERATION
                   src/insights/
                          |
                          v
                STREAMLIT APPLICATION
                  app.py and pages/
                          |
                          v
                  RESULTS AND EXPORTS
                   src/reporting/
```

*The diagram represents the intended processing architecture. Actual data flow depends on the connector, source availability, dataset schema, and implemented application behavior.*

### Architecture components

| Layer            | Responsibility                                                         |
| ---------------- | ---------------------------------------------------------------------- |
| Ingestion        | Retrieve or load data through supported connectors.                    |
| Validation       | Assess completeness, uniqueness, and configured data constraints.      |
| Processing       | Prepare records and derive supported analytical variables.             |
| Analysis         | Calculate descriptive statistics, relationships, and outlier profiles. |
| Machine learning | Apply implemented models to suitable numerical data.                   |
| Insights         | Organize analytical results and associated evidence.                   |
| Interface        | Provide interactive exploration through Streamlit pages.               |
| Reporting        | Export supported results and research summaries.                       |

---

## 🧪 Scientific and Analytical Approach

### Data quality

Data quality checks help identify issues that may affect interpretation, including:

* Missing or incomplete values.
* Duplicate records.
* Unexpected data types or formats.
* Values outside configured physical or domain-specific bounds.

An observation outside an expected range should be flagged for investigation, not automatically removed. Validation limits must be appropriate for the variable, units, experimental conditions, and source documentation.

### Statistical analysis

For supported numerical variables, the platform can be used to examine:

* Descriptive statistics and quantiles.
* Distribution patterns.
* Pearson and Spearman correlations, where implemented.
* Interquartile range (IQR) outlier profiles.

Correlation describes an association between variables; it does not, by itself, establish causation.

### Machine-learning analysis

FIREWISE-X includes a machine-learning module intended for exploratory analysis of unusual data patterns.

The project documentation describes Isolation Forest and K-Means approaches. Their availability, implementation details, input requirements, and evaluation results should be checked against the current source code before interpreting model outputs.

* **Isolation Forest:** identifies observations that are relatively easy to isolate from the rest of a dataset.
* **K-Means:** groups observations according to their distance from cluster centers.
* **IQR analysis:** identifies observations outside selected statistical fences.

These techniques require suitable numerical features and appropriate preprocessing. Results depend on the dataset, selected parameters, and assumptions. They do not independently establish physical causes or predict real-world fire outcomes.

---

## 🛰️ Data Sources and Provenance

The project is designed to explore combustion research associated with the following resources:

| Resource                             | Research context                                                          |
| ------------------------------------ | ------------------------------------------------------------------------- |
| NASA Technical Reports Server (NTRS) | NASA technical publications and research reports.                         |
| BASS-II                              | Burning and suppression of solid materials in microgravity research.      |
| Saffire                              | Spacecraft fire-safety experiments conducted using Cygnus cargo vehicles. |
| SoFIE                                | Solid Fuel Ignition and Extinction research in the space environment.     |

### Source verification

The presence of a connector in the code does not guarantee that a live endpoint is available, that its response contains raw experimental measurements, or that its schema is compatible with every analysis.

For reproducible interpretation, users should check:

* The original source and record identifier.
* Whether the information is a publication, experimental record, or numerical measurement.
* Retrieval time and cache status, when available.
* Units, variable definitions, and experimental conditions.
* Whether the data are measured, derived, or calculated by the application.

NASA publications and experiment descriptions may provide valuable scientific context without providing a directly downloadable numerical dataset. Data availability and access methods can vary by resource.

For source-specific details and known access limitations, see [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

---

## 💻 Technology Stack

The project is organized around the following technologies, subject to the dependencies and implementations in the current repository.

| Technology                       | Purpose                                                                  |
| -------------------------------- | ------------------------------------------------------------------------ |
| Python                           | Application logic and scientific computing.                              |
| Streamlit                        | Interactive web application and dashboard.                               |
| Pandas                           | Tabular data handling and analysis.                                      |
| NumPy                            | Numerical calculations and analytical operations.                        |
| Plotly                           | Interactive scientific visualizations, where used.                       |
| Requests / Python HTTP utilities | Online data retrieval, where configured.                                 |
| Pytest                           | Automated testing.                                                       |
| Custom analytical modules        | Data validation, statistical analysis, anomaly detection, and reporting. |

The project also contains an `src/ml/` module for analytical models. Refer to the source code and `requirements.txt` for the exact implementation and installed dependencies.

---

## 📁 Project Structure

```text
FIREWISE-X/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── components/
│   ├── __init__.py
│   ├── auth.py
│   ├── charts.py
│   ├── evidence_cards.py
│   ├── navigation.py
│   ├── source_status.py
│   └── styles.py
│
├── pages/
│   ├── 1_Research_Explorer.py
│   ├── 2_Data_Quality.py
│   ├── 3_Scientific_Analysis.py
│   ├── 4_Anomaly_Explorer.py
│   ├── 5_Evidence_and_Insights.py
│   ├── 6_About_and_Methodology.py
│   └── 7_Data_Import_and_Export.py
│
├── src/
│   ├── config.py
│   ├── ingestion/
│   ├── validation/
│   ├── processing/
│   ├── analysis/
│   ├── ml/
│   ├── insights/
│   └── reporting/
│
├── tests/
│   ├── __init__.py
│   ├── acceptance_live_test.py
│   ├── test_analysis.py
│   ├── test_ingestion.py
│   ├── test_refresh.py
│   └── test_validation.py
│
└── docs/
    ├── DATA_SOURCES.md
    ├── DEMO_SCRIPT.md
    ├── LIMITATIONS.md
    └── METHODOLOGY.md
```

Some folders contain additional implementation files. Consult the repository for the complete source tree.

---

## ⚙️ Installation and Setup

### Prerequisites

* Python installed on your system.
* Git, if cloning the repository.
* An internet connection for online data sources that are available and supported.
* Windows PowerShell, Command Prompt, or another compatible terminal.

### 1. Clone the repository

```powershell
git clone https://github.com/keerthivhx/FIREWISE-X.git
cd FIREWISE-X
```

If you already have the project locally, navigate to its folder instead.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can allow script execution for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Run the automated tests

```powershell
python -m pytest -v
```

Review the test output to determine which tests passed, failed, or were skipped.

### 6. Run the live-data acceptance test

```powershell
python -m tests.acceptance_live_test
```

This test may require network connectivity and access to the configured endpoints. A successful local test run should not be assumed until the command has actually completed successfully.

### 7. Launch the application

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

Keep the terminal open while using the application.

---

## 🧭 How to Use FIREWISE-X

### Explore research data

Open **Research Explorer** to browse the data available to the application and inspect individual records where supported.

### Examine data quality

Open **Data Quality** to review missing values, duplicate records, and configured validation checks.

### Analyze scientific relationships

Open **Scientific Analysis** to explore distributions, numerical summaries, and relationships between supported variables.

### Investigate unusual observations

Open **Anomaly Explorer** to examine statistical outliers or model-flagged observations. Review the underlying measurements and experimental context before interpreting them.

### Review evidence and insights

Open **Evidence and Insights** to examine generated findings and their supporting source information, where available.

### Understand the methodology

Open **About and Methodology** for the scientific background, analytical approach, and project limitations.

### Import and export data

Open **Data Import and Export** to use the supported custom-data formats and reporting options. Check the interface for accepted file types and available export formats.

### Refresh online data

If the application exposes a source selector or refresh control, use it to select a supported source or request an updated retrieval. Confirm the displayed source status and retrieval outcome rather than assuming that a refresh succeeded.

---

## 🔬 Scientific Integrity

FIREWISE-X is intended to make scientific data easier to inspect without overstating what the analysis establishes.

Our guiding principles are:

1. **Preserve provenance:** retain available information about where records originate.
2. **Distinguish observation from inference:** separate source measurements from derived values and model-generated findings.
3. **Avoid silent data removal:** flag suspicious values for review rather than discarding them without explanation.
4. **Make assumptions visible:** document units, filters, thresholds, and analytical parameters where applicable.
5. **Avoid unsupported causal claims:** statistical associations and anomalies are not proof of physical mechanisms.
6. **Report uncertainty and limitations:** analytical results are only as reliable as the source data, assumptions, and methods used.
7. **Verify before presenting:** claims about live data, model performance, and test coverage must be supported by actual execution or documented evidence.

The application should not be treated as a replacement for validated spacecraft fire-safety procedures, laboratory experiments, or expert engineering assessment.

---

## ⚠️ Limitations and Future Work

### Current limitations

* Online sources may be unavailable, change their response formats, or provide publications rather than raw measurements.
* Different experiments may use different variables, units, measurement methods, and operating conditions.
* Statistical relationships do not establish causality.
* Anomaly detection can flag valid extreme measurements as well as data errors.
* Model results depend on feature selection, preprocessing, parameter settings, and the quantity and quality of available data.
* Exploratory findings require domain-expert interpretation before they can inform practical fire-safety decisions.
* Live-data access, scientific validity, and test coverage must be verified for the specific version being demonstrated.

### Potential future improvements

* Expand support for well-documented, downloadable experimental datasets.
* Add source-specific schema validation and stronger data provenance tracking.
* Improve uncertainty reporting and comparisons across experiments.
* Add model evaluation using appropriately labelled or independently validated observations.
* Improve reproducibility through versioned datasets, recorded parameters, and exportable analysis metadata.
* Explore relevant NASA Open Science Data Repository resources where scientifically appropriate and supported by available data.

See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) and [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for additional project documentation.

---

## 🚀 Project Vision

FIREWISE-X aims to bridge the gap between space combustion research and accessible scientific data analysis.

By combining data exploration, quality assessment, statistical methods, anomaly investigation, and evidence-oriented reporting, the project provides a foundation for studying how combustion behavior changes in microgravity and how those findings may inform further fire-safety research.

**From Flame in Freefall to Better Scientific Understanding.**

---

## 👥 Challenge Information

**Project:** FIREWISE-X
**Challenge:** NASA Space Apps Challenge 2026
**Challenge theme:** Flame in Freefall
**Repository:** [github.com/keerthivhx/FIREWISE-X](https://github.com/keerthivhx/FIREWISE-X)

*FIREWISE-X is an independent challenge project and is not an official NASA product or an endorsement by NASA.*

---

## 📄 License

A license has not been specified in this README. Add a `LICENSE` file and name the selected license here before redistributing the project under explicit open-source terms.
