"""
NASA Technical Reports Server (NTRS) Scientific Connector
Provides live access to NASA technical papers, experiment reports, and investigation findings
regarding Saffire, SoFIE, ACME, and spacecraft fire safety protocols.
"""

from typing import Dict, Any, Tuple, Optional
import requests
import pandas as pd

from src.ingestion.base import BaseDataConnector
from src.config import ENDPOINTS, DEFAULT_TIMEOUT, USER_AGENT

class NASANtrsConnector(BaseDataConnector):
    """Connector for querying the live NASA NTRS REST API."""

    def __init__(self, query: str = "saffire microgravity flame", max_records: int = 50):
        super().__init__(
            name="NASA Technical Reports Server (NTRS)",
            source_url=ENDPOINTS["NASA_NTRS_SEARCH"],
            cache_file=f"ntrs_{query.replace(' ', '_')}.csv"
        )
        self.query = query
        self.max_records = max_records

    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        headers = {"User-Agent": USER_AGENT}
        params = {
            "q": self.query,
            "size": self.max_records
        }

        resp = requests.get(self.source_url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()

        data = resp.json()
        results = data.get("results", [])

        records = []
        for item in results:
            # Parse downloads info
            downloads = item.get("downloads", [])
            pdf_url = None
            fulltext_url = None
            if downloads and isinstance(downloads, list):
                first_dl = downloads[0]
                links = first_dl.get("links", {})
                if links.get("pdf"):
                    pdf_url = "https://ntrs.nasa.gov" + links.get("pdf")
                if links.get("fulltext"):
                    fulltext_url = "https://ntrs.nasa.gov" + links.get("fulltext")

            # Authors
            authors = []
            for aff in item.get("authorAffiliations", []):
                meta = aff.get("meta", {})
                if meta.get("author", {}).get("name"):
                    authors.append(meta["author"]["name"])

            records.append({
                "citation_id": item.get("id"),
                "title": item.get("title"),
                "publication_date": item.get("publicationDate") or item.get("created"),
                "center": item.get("center"),
                "sti_type": item.get("stiType"),
                "subject_categories": ", ".join(item.get("subjectCategories", [])) if item.get("subjectCategories") else "",
                "authors": "; ".join(authors[:5]) + ("..." if len(authors) > 5 else ""),
                "abstract": item.get("abstract", ""),
                "pdf_url": pdf_url,
                "fulltext_url": fulltext_url,
                "is_saffire": "saffire" in (item.get("title", "") + item.get("abstract", "")).lower(),
                "is_sofie": "sofie" in (item.get("title", "") + item.get("abstract", "")).lower()
            })

        df = pd.DataFrame(records)

        extra_meta = {
            "query": self.query,
            "api_endpoint": self.source_url,
            "total_hits_reported": data.get("total"),
            "retrieved_count": len(df),
            "source_type": "Live Official NASA REST API",
            "license": "NASA Public Domain / Open Access"
        }

        return df, extra_meta

    def describe_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": (
                "Official NASA Technical Reports Server REST API providing authoritative publications, "
                "flight investigation syntheses, engineering models, and flight test summaries for Saffire and SoFIE."
            ),
            "measurements": {
                "citation_id": "Unique NASA scientific report identifier",
                "title": "Title of research paper or flight experiment technical report",
                "publication_date": "Publication or release timestamp",
                "center": "NASA research center responsible (e.g., GRC - Glenn Research Center)",
                "subject_categories": "Scientific taxonomy category",
                "abstract": "Authoritative summary of experimental findings and parameters",
                "pdf_url": "Direct NASA STI repository link to the complete technical document"
            },
            "source_type": "Live REST API",
            "access_restrictions": "None (Public NASA Open Science endpoint)",
            "limitations": "Returns bibliographic, documentary, and qualitative synthesis data rather than time-series numerical tables."
        }
