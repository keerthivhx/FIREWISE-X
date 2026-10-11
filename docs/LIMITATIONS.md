# FIREWISE-X: Scientific Boundaries & System Limitations

This document states the scientific, data, model, and operational boundaries of **FIREWISE-X** to ensure rigorous, responsible deployment.

---

## 1. Scientific & Operational Boundaries

* **Not a Spacecraft Flight Alarm System:**
  FIREWISE-X is an offline/online scientific analysis and research exploration platform. It is **not** an operational avionics system and does not replace NASA Caution & Warning (C&W), Fire Detection and Suppression (FDS), or Environmental Control and Life Support System (ECLSS) hardware aboard the ISS, Orion, or commercial space stations.
* **Archival Flight Datasets vs. Live Telemetry:**
  NASA does not expose continuous raw telemetry from the ISS or Cygnus to unauthenticated public internet sockets due to ITAR, EAR, and flight safety constraints. Telemetry analyzed herein represents completed, peer-reviewed flight test runs released via NASA PSI and NTRS.
* **Absence of Real-Time Microgravity Sensor Stream:**
  The application clearly flags data age and freshness. It never fabricates simulated real-time sensor streams or masquerades historical files as live telemetry.

---

## 2. Machine Learning Limitations

* **Unsupervised Anomaly Interpretation:**
  Isolation Forest and IQR anomaly detectors flag points that deviate mathematically from the majority of experimental runs. **An anomaly does not equate to a spacecraft fire catastrophe.** Outliers often correspond to:
  * Deliberate high-flow forced-convection boundary limit tests.
  * Rapidly quenched runs where ignition failed.
  * Unusual sample geometries (e.g. solid spheres vs. thin films).
* **Sample Size & Feature Sparsity:**
  Flight combustion experiments are resource-intensive; datasets typically range between 50 and 200 physical test runs. Complex deep neural networks are prone to severe overfitting on such sample sizes; hence, robust tree ensembles (Isolation Forest) and linear correlations are strictly enforced.

---

## 3. Network & Service Dependencies

* **NASA REST API Availability:**
  The NTRS connector relies on the uptime of `https://ntrs.nasa.gov`. If NASA STI servers undergo scheduled maintenance, FIREWISE-X automatically serves cached records and warns the user with the timestamp of the last successful synchronization.
* **Direct GRC/PSI Access:**
  Direct internal Glenn Research Center repositories (`gipoc.grc.nasa.gov`) enforce institutional security certificates. FIREWISE-X routes access through public open science mirrors and NASA STI indexes.
