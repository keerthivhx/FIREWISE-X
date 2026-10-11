"""
Unit Tests for Cache Refresh & Network Failure Recovery
"""

import pandas as pd
from unittest.mock import patch, MagicMock
from src.ingestion.base import BaseDataConnector

class ResilientConnector(BaseDataConnector):
    def __init__(self, cache_file="resilient_test.csv"):
        super().__init__(
            name="Resilient Connector",
            source_url="https://api.nasa.gov/resilient",
            cache_file=cache_file,
            ttl_seconds=3600
        )
        self.should_fail = False

    def fetch_online(self):
        if self.should_fail:
            raise ConnectionError("Simulated Network Timeout / DNS Failure")
        return pd.DataFrame({"run_id": [101, 102], "flame_speed": [2.3, 2.7]}), {"source": "online"}

    def describe_capabilities(self):
        return {"name": self.name}


def test_failed_refresh_preserves_valid_cache():
    conn = ResilientConnector()

    # Step 1: Successful initial retrieval
    df1, meta1 = conn.fetch_data(force_refresh=True)
    assert len(df1) == 2
    assert meta1["freshness_type"] == "Online Retrieval (Fresh)"

    # Step 2: Network failure during force refresh
    conn.should_fail = True
    df2, meta2 = conn.fetch_data(force_refresh=True)

    # Should gracefully return previously cached data with explicit warning
    assert len(df2) == 2
    assert "Fallback" in meta2["freshness_type"]
    assert "warning" in meta2
    assert "Network Timeout" in meta2["warning"]
