# FIREWISE-X: Competition Demonstration Script (NASA Space Apps 2026)

**Demonstration Goal:** Present a clear, rigorous, data-backed 3-minute walkthrough for competition evaluators, proving that the application is online-driven, reproducible, and scientifically grounded.

---

## Step 1: The Core Scientific Problem (30 seconds)
* **What to show:** Home Dashboard (`app.py`).
* **What to say:**
  > "In terrestrial fire safety, hot gases rise naturally due to buoyant convection, feeding fresh oxygen to the flame. In the microgravity of space stations and transit spacecraft, buoyancy vanishes. Flames become spherical diffusion envelopes, burn at lower temperatures, and can smolder silently in ventilation dead zones.
  >
  > Welcome to FIREWISE-X: an AI-powered scientific exploration platform translating authentic NASA microgravity combustion datasets into actionable spacecraft fire safety insights."

---

## Step 2: Genuine Online Data Provenance (45 seconds)
* **What to show:** Top Status Banner and Telemetry Taxonomy expander.
* **What to say:**
  > "Notice the status banner at the top: FIREWISE-X adheres to a strict no-hardcoded-data policy. We are connected directly to the NASA ISS BASS-II flight repository and the live NASA Technical Reports Server (NTRS) REST API.
  >
  > The banner shows real connection health, exact ISO-8601 retrieval timestamps, and record counts (129 flight tests). Every metric you see—from baseline oxygen concentration to toxic carbon monoxide generation—is calculated reactively from the underlying data."

---

## Step 3: Scientific Data Quality & Validation (30 seconds)
* **What to show:** Navigate to **Page 2: Data Quality**.
* **What to say:**
  > "Before running any analysis, FIREWISE-X audits the dataset. Here we see our Data Health Score of 94.4/100, auditing completeness, uniqueness, and physical boundary constraints.
  >
  > In microgravity combustion, missing values often mean quenched tests rather than corrupted data. Our pipeline logs every cleaning step transparently without silently discarding valid scientific observations."

---

## Step 4: Empirical Analysis & Trends (30 seconds)
* **What to show:** Navigate to **Page 3: Scientific Analysis**.
* **What to say:**
  > "In the Scientific Analysis Engine, we observe the correlation matrix and custom scatter plots. For example, comparing forced ventilation (fan display speed) against Carbon Monoxide generation reveals how cabin airflow drives toxic product accumulation.
  >
  > If we switch data sources or filter by fuel type—such as PMMA film versus Cotton—the charts and statistical metrics update dynamically."

---

## Step 5: Machine Learning Anomaly Detection (30 seconds)
* **What to show:** Navigate to **Page 4: Anomaly Explorer**.
* **What to say:**
  > "We do not claim our ML model replaces NASA caution systems. Instead, we train a pure Isolation Forest on multi-dimensional combustion parameters (O2 consumption, fan speed, CO output) to detect rare operating regimes.
  >
  > Evaluators can inspect the exact flagged outliers and read the physical justification for why each test point diverged."

---

## Step 6: Evidence Insights & Export (15 seconds)
* **What to show:** Navigate to **Page 5: Evidence & Insights** and **Page 7: Data Import & Export**.
* **What to say:**
  > "Finally, our Evidence Engine converts findings into structured dossiers with citations, methodology, and limitations, which evaluators can download directly as reproducible Markdown and CSV files.
  >
  > FIREWISE-X delivers an honest, rigorous, online data platform for the future of spaceflight fire safety."
