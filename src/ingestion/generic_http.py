"""
Generic HTTP Scientific Data Connector
Allows retrieving public scientific datasets from custom endpoints (CSV, JSON, etc.)
with size limits, timeout guards, and content-type validation.
"""

from typing import Dict, Any, Tuple
import io
import requests
import pandas as pd

from src.ingestion.base import BaseDataConnector
from src.config import DEFAULT_TIMEOUT, USER_AGENT

MAX_ALLOWED_BYTES = 50 * 1024 * 1024  # 50 MB safety limit

class GenericHttpConnector(BaseDataConnector):
    """Retrieves external datasets from user-specified scientific URLs."""

    def __init__(self, endpoint_url: str, custom_name: str = "External Scientific Endpoint"):
        cache_key = "".join(c for c in endpoint_url if c.isalnum())[-24:] or "custom"
        super().__init__(
            name=custom_name,
            source_url=endpoint_url,
            cache_file=f"generic_{cache_key}.csv"
        )

    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        headers = {"User-Agent": USER_AGENT}

        # Check headers first
        head_resp = requests.head(self.source_url, headers=headers, timeout=5, allow_redirects=True)
        content_length = head_resp.headers.get("content-length")
        if content_length and int(content_length) > MAX_ALLOWED_BYTES:
            raise ValueError(f"File size exceeds safety limit ({int(content_length)/(1024*1024):.1f} MB > 50 MB)")

        resp = requests.get(self.source_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "").lower()

        # Reject HTML error pages disguised as 200
        if "text/html" in content_type:
            raise ValueError("Endpoint returned HTML web page instead of structured data (CSV/JSON).")

        # Try parsing as CSV or JSON
        try:
            if "json" in content_type or self.source_url.endswith(".json"):
                data = resp.json()
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                elif isinstance(data, dict):
                    # Find first list value if nested
                    list_keys = [k for k, v in data.items() if isinstance(v, list)]
                    if list_keys:
                        df = pd.DataFrame(data[list_keys[0]])
                    else:
                        df = pd.DataFrame([data])
                else:
                    raise ValueError("JSON structure is not tabular.")
            else:
                # Default to CSV
                df = pd.read_csv(io.BytesIO(resp.content), encoding="utf-8-sig")
        except Exception as e:
            raise ValueError(f"Failed to parse tabular data from endpoint: {e}")

        extra_meta = {
            "content_type": content_type,
            "bytes_received": len(resp.content),
            "source_type": "Custom Scientific URL"
        }

        return df, extra_meta

    def describe_capabilities(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": f"Custom user-configured dataset retrieved from {self.source_url}",
            "measurements": "Dynamic schema detected on retrieval",
            "source_type": "External HTTP Endpoint",
            "access_restrictions": "Determined by host server",
            "limitations": "Subject to availability and format consistency of host server."
        }
