"""
NASA SoFIE (Solid Fuel Ignition and Extinction) Investigation Connector
Fetches published research records and experimental parameters for the SoFIE facility
onboard the International Space Station Combustion Integrated Rack (CIR).
"""

from typing import Dict, Any, Tuple
import requests
import pandas as pd

from src.ingestion.base import BaseDataConnector
from src.config import ENDPOINTS, DEFAULT_TIMEOUT, USER_AGENT
from src.ingestion.nasa_ntrs import NASANtrsConnector

class NASASofieConnector(BaseDataConnector):
    """Connector for NASA SoFIE (Solid Fuel Ignition and Extinction) research data."""

    def __init__(self):
        super().__init__(
            name="NASA SoFIE CIR Investigation Records",
            source_url=ENDPOINTS["NASA_SOFIE_INFO"],
            cache_file="sofie_investigation_records.csv"
        )
        self.ntrs_helper = NASANtrsConnector(query="SoFIE solid fuel ignition extinction microgravity", max_records=25)

    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        # Portal accessibility check
        portal_status = "Main portal requires browser session; accessing via official NASA STI"
        try:
            resp = requests.get(self.source_url, timeout=5, headers={"User-Agent": USER_AGENT})
            if resp.status_code == 200:
                portal_status = "Direct portal accessible"
        except Exception as e:
            portal_status = f"Portal note: {type(e).__name__} (routed to NTRS API)"

        df_ntrs, meta_ntrs = self.ntrs_helper.fetch_data(force_refresh=True)

        if df_ntrs.empty:
            raise ValueError("No SoFIE records returned from NASA NTRS repository.")

        df = df_ntrs.copy()
        df["sub_investigation"] = df["title"].apply(self._detect_sub_investigation)

        extra_meta = {
            "facility": "Combustion Integrated Rack (CIR) in the Destiny module on ISS",
            "chamber": "Flow Duct Insert within CIR",
            "sub_projects": [
                "GEL (Growth and Extinction Limit)",
                "MIST (Material Ignition and Suppression Test)",
                "narrow channel flame spread",
                "residence time effects"
            ],
            "portal_status": portal_status,
            "source_type": "NASA NTRS REST API Verification"
        }

        return df, extra_meta

    @staticmethod
    def _detect_sub_investigation(title: str) -> str:
        t = str(title).upper()
        if "GEL" in t or "GROWTH AND EXTINCTION" in t:
            return "SoFIE-GEL"
        elif "MIST" in t:
            return "SoFIE-MIST"
        elif "RESIDENCE TIME" in t:
            return "SoFIE-RT"
        elif "NARROW CHANNEL" in t:
            return "SoFIE-NC"
        return "SoFIE Core Science"

    def describe_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": (
                "Technical records for NASA's SoFIE project on the ISS Combustion Integrated Rack (CIR). "
                "Studies radiative extinction, opposed flow flammability, and thick fuel sample ignition."
            ),
            "measurements": {
                "sub_investigation": "Specific SoFIE sub-study (GEL, MIST, RT, etc.)",
                "title": "NASA scientific publication title",
                "publication_date": "Publication timestamp",
                "abstract": "Summary of experimental findings, oxidizer flows, and extinction limits"
            },
            "source_type": "NASA Official Scientific Technical Information Repository",
            "access_restrictions": "Publicly accessible via NTRS",
            "limitations": "Ongoing flight experiment series; flight raw sensor telemetry releases are subject to NASA PSI curation."
        }
