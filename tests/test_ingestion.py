"""
Unit and Integration Tests for FIREWISE-X Ingestion Layer
Verifies online connectors, caching, error recovery, and provenance tracking.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from src.ingestion.base import BaseDataConnector
from src.ingestion.generic_http import GenericHttpConnector
from src.ingestion.nasa_bass import NASABass2Connector
from src.ingestion.nasa_ntrs import NASANtrsConnector

class MockConnector(BaseDataConnector):
    """Concrete connector subclass for unit testing base caching behavior."""
    def __init__(self, cache_file="test_cache.csv"):
        super().__init__(
            name="Mock Test Connector",
            source_url="https://api.nasa.gov/mock/test",
            cache_file=cache_file,
            ttl_seconds=60
        )
        self.mock_records = pd.DataFrame({"id": [1, 2, 3], "value": [10.5, 20.1, 30.2]})

    def fetch_online(self):
        return self.mock_records, {"mock_key": "mock_value"}

    def describe_capabilities(self):
        return {"name": self.name}


def test_base_connector_caching_and_provenance(tmp_path):
    """Tests that first fetch caches data and subsequent fetch retrieves from cache within TTL."""
    conn = MockConnector(cache_file="temp_mock.csv")
    df, meta = conn.fetch_data(force_refresh=True)

    assert not df.empty
    assert len(df) == 3
    assert meta["source_name"] == "Mock Test Connector"
    assert meta["freshness_type"] == "Online Retrieval (Fresh)"
    assert conn.cache_path.exists()

    # Second fetch without force_refresh should load from cache
    df2, meta2 = conn.fetch_data(force_refresh=False)
    assert len(df2) == 3
    assert "Cached" in meta2["freshness_type"]


def test_generic_http_connector_rejects_html():
    """Ensures that HTML error pages disguised as 200 responses are rejected."""
    conn = GenericHttpConnector("https://example.com/fake.csv")
    with patch("requests.head") as mock_head, patch("requests.get") as mock_get:
        mock_head.return_value = MagicMock(headers={"content-length": "1000"})
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"content-type": "text/html; charset=utf-8"}
        mock_resp.content = b"<html><body>Error 404 Not Found</body></html>"
        mock_get.return_value = mock_resp

        with pytest.raises(ValueError, match="HTML web page"):
            conn.fetch_online()


def test_nasa_ntrs_connector_mock():
    """Tests parsing of NASA NTRS API JSON responses."""
    conn = NASANtrsConnector(query="test", max_records=5)
    mock_data = {
        "total": 1,
        "results": [{
            "id": "20240001",
            "title": "Saffire Flame Behavior in Low Gravity",
            "publicationDate": "2024-05-01",
            "center": "GRC",
            "stiType": "CONFERENCE_PAPER",
            "subjectCategories": ["Combustion"],
            "abstract": "Microgravity flame dynamics during Saffire.",
            "downloads": []
        }]
    }

    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_data
        mock_get.return_value = mock_resp

        df, meta = conn.fetch_online()
        assert len(df) == 1
        assert df.iloc[0]["citation_id"] == "20240001"
        assert bool(df.iloc[0]["is_saffire"]) is True
        assert meta["total_hits_reported"] == 1
