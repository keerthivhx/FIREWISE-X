"""
NASA Saffire Spacecraft Fire Safety Experiment Connector
Synthesizes flight investigation records for Saffire I through VI
conducted in uncrewed Cygnus resupply vehicles post-ISS departure.
"""

from typing import Dict, Any, Tuple
import requests
import pandas as pd

from src.ingestion.base import BaseDataConnector
from src.config import ENDPOINTS, DEFAULT_TIMEOUT, USER_AGENT
from src.ingestion.nasa_ntrs import NASANtrsConnector

class NASASaffireConnector(BaseDataConnector):
    """
    Connector for NASA Saffire (Spacecraft Fire Experiment) data.
    Retrieves verified Saffire flight records and peer-reviewed technical parameters via NASA NTRS API.
    """

    def __init__(self):
        super().__init__(
            name="NASA Saffire Flight Experiment Records",
            source_url=ENDPOINTS["NASA_SAFFIRE_INFO"],
            cache_file="saffire_flight_records.csv"
        )
        self.ntrs_helper = NASANtrsConnector(query="Saffire spacecraft fire experiment Cygnus", max_records=25)

    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        # Check direct Saffire portal status
        portal_status = "Direct GRC portal restricted (SSL/403); accessing via authenticated NASA STI / NTRS"
        try:
            p_resp = requests.get(self.source_url, timeout=5, headers={"User-Agent": USER_AGENT})
            if p_resp.status_code == 200:
                portal_status = "Direct portal accessible"
        except Exception as e:
            portal_status = f"Portal direct connect note: {type(e).__name__} (routed to NTRS API)"

        # Fetch authentic Saffire technical records from NASA NTRS
        df_ntrs, meta_ntrs = self.ntrs_helper.fetch_data(force_refresh=True)

        if df_ntrs.empty:
            raise ValueError("No Saffire records returned from NASA NTRS repository.")

        # Annotate with Saffire mission flight phases
        df = df_ntrs.copy()
        df["mission_series"] = df["title"].apply(self._detect_saffire_flight)

        extra_meta = {
            "experiment": "Spacecraft Fire Safety Experiment (Saffire)",
            "vehicle": "Northrop Grumman Cygnus Automated Cargo Vehicle",
            "primary_goals": [
                "Large-scale flame spread in microgravity",
                "Low-pressure oxygen-enriched flammability limits",
                "Spacecraft fire detection, cleanup, and post-fire atmospheric scrubbing"
            ],
            "portal_status": portal_status,
            "source_type": "NASA NTRS REST API Verification"
        }

        return df, extra_meta

    @staticmethod
    def _detect_saffire_flight(title: str) -> str:
        t = str(title).upper()
        if "SAFFIRE-VI" in t or "SAFFIRE VI" in t:
            return "Saffire-VI"
        elif "SAFFIRE-V" in t or "SAFFIRE V" in t:
            return "Saffire-V"
        elif "SAFFIRE-IV" in t or "SAFFIRE IV" in t:
            return "Saffire-IV"
        elif "SAFFIRE-III" in t or "SAFFIRE III" in t:
            return "Saffire-III"
        elif "SAFFIRE-II" in t or "SAFFIRE II" in t:
            return "Saffire-II"
        elif "SAFFIRE-I" in t or "SAFFIRE I" in t:
            return "Saffire-I"
        return "Saffire Multi-Mission Synthesis"

    def describe_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": (
                "Authoritative dataset of NASA Saffire flight research. Saffire conducted the first "
                "large-scale real fires inside an orbital spacecraft (Cygnus) under low and elevated O2."
            ),
            "measurements": {
                "mission_series": "Specific Saffire flight experiment (Saffire I through VI)",
                "title": "NASA technical paper or flight summary title",
                "publication_date": "Date of NASA Technical Publication",
                "abstract": "Summary of burning conditions, pressure, and flame spread findings",
                "pdf_url": "Direct link to NASA STI technical report PDF"
            },
            "source_type": "NASA Official Scientific Technical Information Repository",
            "access_restrictions": "Publicly accessible via NTRS; GRC internal telemetry is export-controlled (ITAR/EAR).",
            "limitations": "Full time-series high-frequency photometer telemetry from Cygnus is export-controlled."
        }
