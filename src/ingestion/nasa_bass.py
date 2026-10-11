"""
NASA BASS-II Microgravity Flight Combustion Data Connector
Fetches genuine BASS-II (Burning and Suppression of Solids - II) experimental records
conducted aboard the International Space Station (ISS) in the Microgravity Science Glovebox.
"""

from typing import Dict, Any, Tuple
import io
import requests
import pandas as pd

from src.ingestion.base import BaseDataConnector
from src.config import ENDPOINTS, DEFAULT_TIMEOUT, USER_AGENT

class NASABass2Connector(BaseDataConnector):
    """Connector for the NASA PSI BASS-II flight combustion experiment dataset."""

    def __init__(self):
        super().__init__(
            name="NASA ISS BASS-II Flight Experiment",
            source_url=ENDPOINTS["NASA_BASS2_DATASET"],
            cache_file="bass2_experiments.csv"
        )

    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(self.source_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()

        # Parse CSV handling utf-8-sig (BOM)
        content_text = resp.content.decode("utf-8-sig", errors="replace")
        df_raw = pd.read_csv(io.StringIO(content_text))

        # Standardize column mapping while preserving original names
        col_mapping = {
            "PI": "principal_investigator",
            "Test #": "test_id",
            "Date": "date",
            "GMT": "gmt_time",
            "Sample #": "sample_id",
            "Fuel Sample Material": "fuel_material",
            "Flow restrictor": "flow_restrictor",
            "Fan display": "fan_display",
            "Air display": "air_display",
            "Total Frames Shot": "total_frames",
            "Calibrated  initial O2 % by vol ": "initial_o2_pct",
            "Calibrated final O2 % by vol": "final_o2_pct",
            "Initial CO2 % by vol": "initial_co2_pct",
            "Final CO2 % by vol": "final_co2_pct",
            "Initial CO (ppm)": "initial_co_ppm",
            "Final CO (ppm)": "final_co_ppm"
        }

        # Handle variations in radiometer gain column name
        for col in df_raw.columns:
            if "radiometer" in col.lower() or "gain" in col.lower():
                col_mapping[col] = "radiometer_gain"

        df = df_raw.rename(columns=col_mapping)

        # Clean string/whitespace fields
        for str_col in ["principal_investigator", "test_id", "fuel_material"]:
            if str_col in df.columns:
                df[str_col] = df[str_col].astype(str).str.strip()

        # Extract fuel category (PMMA, Cotton, Nomex, Silicone, etc.)
        if "fuel_material" in df.columns:
            df["fuel_category"] = df["fuel_material"].apply(self._classify_fuel)

        extra_meta = {
            "experiment_facility": "Microgravity Science Glovebox (MSG) on ISS",
            "pi": "Prof. Subrata Bhattacharjee (San Diego State University / NASA GRC)",
            "investigation": "Burning and Suppression of Solids - II (BASS-II)",
            "primary_measurements": [
                "Oxygen Concentration (% vol)",
                "Carbon Dioxide Generation (% vol)",
                "Carbon Monoxide Generation (ppm)",
                "Flow & Fan speed display",
                "Radiometer Gain"
            ],
            "original_columns": list(df_raw.columns)
        }

        return df, extra_meta

    @staticmethod
    def _classify_fuel(fuel_str: str) -> str:
        s = str(fuel_str).lower()
        if "pmma" in s:
            if "100" in s:
                return "PMMA Thin (100 µm)"
            elif "200" in s:
                return "PMMA Medium (200 µm)"
            elif "rod" in s or "thick" in s:
                return "PMMA Rod/Thick"
            return "PMMA Film"
        elif "cotton" in s:
            return "Cotton Fabric"
        elif "nomex" in s:
            return "Nomex Blend"
        elif "wax" in s or "paraffin" in s:
            return "Wax/Paraffin"
        elif "sphere" in s:
            return "Solid Sphere Section"
        elif s == "" or s == "nan" or s == "none":
            return "Unspecified"
        return "Specialty Solid Fuel"

    def describe_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": (
                "Direct measurements from 120+ microgravity solid fuel burning tests aboard the ISS. "
                "Examines extinction boundaries, forced flow interactions, and toxic effluent kinetics in μg."
            ),
            "measurements": {
                "initial_o2_pct": "Calibrated initial atmospheric oxygen volume percentage (%)",
                "final_o2_pct": "Post-burn or extinction oxygen volume percentage (%)",
                "initial_co2_pct": "Initial cabin CO2 volume percentage (%)",
                "final_co2_pct": "Final CO2 volume percentage after combustion (%)",
                "initial_co_ppm": "Initial toxic Carbon Monoxide in parts per million (ppm)",
                "final_co_ppm": "Final Carbon Monoxide produced in parts per million (ppm)",
                "flow_restrictor": "Physical restrictor setting controlling glovebox ventilation speed",
                "fan_display": "Fan tachometer reading governing oxidizer flow velocity"
            },
            "source_type": "Curated NASA PSI Flight Data Repository",
            "access_restrictions": "Publicly accessible research data (Open Science)",
            "limitations": (
                "Data represents discrete test runs in the ISS Microgravity Science Glovebox. "
                "Quenched/non-ignited runs have missing final combustion products."
            )
        }
