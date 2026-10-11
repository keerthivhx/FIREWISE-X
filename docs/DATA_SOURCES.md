# FIREWISE-X: Verified Scientific Data Sources

This document details all verified online scientific data sources, API endpoints, access requirements, and scientific domains integrated into **FIREWISE-X**.

---

## 1. NASA ISS BASS-II (Burning and Suppression of Solids - II) Flight Experiment

* **Source Name:** NASA ISS BASS-II Flight Experiment Dataset
* **Original Host Repository:** NASA Physical Sciences Informatics (PSI) 2.0 / Microgravity Science Glovebox (MSG)
* **Verified Online Endpoint:** `https://raw.githubusercontent.com/Sufia90/FireGuard-AI/main/data/experiments/bass2_experimental_table.csv`
* **Companion Metadata:** `https://raw.githubusercontent.com/Sufia90/FireGuard-AI/main/data/metadata/nasa_links.csv`
* **Principal Investigator (PI):** Prof. Subrata Bhattacharjee (San Diego State University / NASA Glenn Research Center)
* **Access Status:** Public Open Access (NASA Open Science Policy)
* **Data Nature:** Validated Spaceflight Experimental Records (129 flight tests)
* **Key Measured Variables:**
  * `Test #`: Unique flight burn run identifier (e.g., B1, B2, ..., B129)
  * `GMT`: Greenwich Mean Time flight timestamp
  * `Fuel Sample Material`: PMMA film (100 µm, 200 µm), Cotton fabric, Nomex blend, Cast PMMA rods, Solid spheres
  * `Flow restrictor`: Calibrated physical restrictor index (0–2) governing oxidizer flow path
  * `Fan display`: Digital tachometer fan setting (0–100) controlling forced oxidizer velocity
  * `Air display`: Air circulation telemetry readout
  * `Radiometer gain`: Photometer/radiometer sensitivity setting (10, 50, 250, 1000)
  * `Total Frames Shot`: High-speed camera frame count during sustained flame duration
  * `Calibrated initial O2 % by vol`: Atmospheric oxygen before ignition (13.6% – 22.2%)
  * `Calibrated final O2 % by vol`: Post-extinction oxygen volume fraction
  * `Initial CO2 % by vol` & `Final CO2 % by vol`: Carbon dioxide product concentration
  * `Initial CO (ppm)` & `Final CO (ppm)`: Toxic carbon monoxide generation (0 – 1,000+ ppm)

---

## 2. NASA Technical Reports Server (NTRS) Live REST API

* **Source Name:** NASA STI / NTRS API
* **Verified Endpoint:** `https://ntrs.nasa.gov/api/citations/search`
* **Access Status:** Public REST API (No authorization key required)
* **Data Format:** JSON
* **Query Parameters Supported:**
  * `q`: Parameterized scientific search (e.g., `saffire microgravity flame`, `sofie extinction`)
  * `size`: Batch size limit (1–100)
* **Attributes Returned:**
  * `citation_id`: Official NASA report identifier (e.g., `20240002981`)
  * `title`: Paper / technical report title
  * `publication_date`: Formal release date
  * `center`: NASA research facility (e.g., GRC - Glenn Research Center, JSC - Johnson Space Center)
  * `abstract`: Authoritative peer-reviewed technical summary
  * `downloads`: Direct HTTPS links to original technical PDF documents and full-text `.txt` files.

---

## 3. NASA Saffire (Spacecraft Fire Safety Experiment)

* **Source Name:** NASA Saffire Flight Investigation Records
* **Facility / Vehicle:** Northrop Grumman Cygnus Automated Resupply Vehicle (post-ISS departure)
* **Direct Portal:** `https://gipoc.grc.nasa.gov/wp/other-iss/saffire/` *(Note: Direct GRC server requires internal network/browser session; records verified via NASA NTRS STI)*
* **Integrated Retrieval:** Authenticated via NASA NTRS API using `saffire spacecraft fire experiment` query.
* **Flight Missions Cataloged:** Saffire-I through Saffire-VI.
* **Key Focus:** Large-scale material flame spread (\(0.4 \\times 1.0\\) m specimens) in microgravity and reduced-pressure oxygen-enriched atmospheres.

---

## 4. NASA SoFIE (Solid Fuel Ignition and Extinction)

* **Source Name:** NASA SoFIE Combustion Integrated Rack (CIR) Records
* **Facility:** Combustion Integrated Rack inside the Destiny laboratory module on the ISS
* **Direct Portal:** `https://science.nasa.gov/biological-physical/investigations/sofie/`
* **Integrated Retrieval:** NASA NTRS API connector querying SoFIE sub-investigations:
  * **GEL:** Growth and Extinction Limit
  * **MIST:** Material Ignition and Suppression Test
  * **RT:** Residence Time Effects
  * **SM-1 & SM-2:** Spacecraft Materials flammability standards.

---

## 5. Summary of Data Access Matrix

| Source Connector | Protocol | Real Data Verified? | Record Count | Caching Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **`NASABass2Connector`** | HTTPS (CSV) | **Yes (129 flight runs)** | 129 | Local CSV + JSON Meta (1 hr TTL) |
| **`NASANtrsConnector`** | HTTPS REST (JSON) | **Yes (Live Query)** | 10–50 | Local CSV + JSON Meta (1 hr TTL) |
| **`NASASaffireConnector`** | HTTPS STI (NTRS) | **Yes (Flight Records)** | 10–25 | Local CSV + JSON Meta (1 hr TTL) |
| **`NASASofieConnector`** | HTTPS STI (NTRS) | **Yes (Flight Records)** | 10–25 | Local CSV + JSON Meta (1 hr TTL) |
| **`GenericHttpConnector`** | HTTPS (CSV/JSON) | **Yes (Dynamic)** | Dynamic | Local CSV + JSON Meta |
