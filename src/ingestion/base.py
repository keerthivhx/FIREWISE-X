"""
Base Data Connector Interface and Cache Management for FIREWISE-X
Provides standard retrieval, caching, error handling, and provenance tracking.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import json
import logging
import pandas as pd

from src.config import CACHE_DIR, DEFAULT_CACHE_TTL

logger = logging.getLogger(__name__)

class BaseDataConnector(ABC):
    """Abstract base connector for all online scientific data sources."""

    def __init__(self, name: str, source_url: str, cache_file: str, ttl_seconds: int = DEFAULT_CACHE_TTL):
        self.name = name
        self.source_url = source_url
        self.cache_path = CACHE_DIR / cache_file
        self.metadata_path = CACHE_DIR / f"{cache_file}.meta.json"
        self.ttl_seconds = ttl_seconds
        self.last_status: str = "Uninitialized"
        self.last_error: Optional[str] = None
        self.last_retrieval_time: Optional[datetime] = None
        self.is_cached: bool = False
        self._load_metadata()

    def _load_metadata(self):
        """Loads cached metadata if present."""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    self.last_retrieval_time = (
                        datetime.fromisoformat(meta["retrieval_time"])
                        if "retrieval_time" in meta and meta["retrieval_time"]
                        else None
                    )
                    self.last_status = meta.get("status", "Cached")
                    self.last_error = meta.get("last_error")
                    self.is_cached = True
            except Exception as e:
                logger.warning(f"Failed to read metadata for {self.name}: {e}")

    def _save_metadata(self, record_count: int, success: bool, error_msg: Optional[str] = None, extra: Optional[Dict] = None):
        """Saves retrieval metadata to disk for traceability."""
        now = datetime.now(timezone.utc)
        meta = {
            "source_name": self.name,
            "source_url": self.source_url,
            "retrieval_time": now.isoformat(),
            "record_count": record_count,
            "status": "Online (Success)" if success else "Failed",
            "last_error": error_msg,
            "extra": extra or {}
        }
        try:
            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            if success:
                self.last_retrieval_time = now
                self.last_status = "Online (Success)"
                self.last_error = None
            else:
                self.last_status = "Error"
                self.last_error = error_msg
        except Exception as e:
            logger.error(f"Could not save metadata: {e}")

    def is_cache_valid(self) -> bool:
        """Checks if cached data exists and is within TTL."""
        if not self.cache_path.exists():
            return False
        if not self.last_retrieval_time:
            return False
        age = (datetime.now(timezone.utc) - self.last_retrieval_time).total_seconds()
        return age < self.ttl_seconds

    @abstractmethod
    def fetch_online(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Connects directly to the public online source and returns (DataFrame, metadata)."""
        pass

    def fetch_data(self, force_refresh: bool = False) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Retrieves data according to online-first policy with graceful offline fallback.
        If force_refresh is True or cache is expired/absent, attempts online retrieval.
        On failure, preserves and returns valid cached data with an explicit error note.
        """
        if not force_refresh and self.is_cache_valid():
            try:
                df = self.load_from_cache()
                self.is_cached = True
                meta = self.get_provenance(len(df))
                meta["freshness_type"] = "Cached (Within TTL)"
                return df, meta
            except Exception as e:
                logger.warning(f"Failed loading cache for {self.name}: {e}")

        # Attempt online retrieval
        try:
            df, extra_meta = self.fetch_online()
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                raise ValueError("Online endpoint returned an empty dataset.")

            # Save to cache
            self.save_to_cache(df)
            self._save_metadata(record_count=len(df), success=True, extra=extra_meta)
            self.is_cached = False
            meta = self.get_provenance(len(df))
            meta["freshness_type"] = "Online Retrieval (Fresh)"
            meta.update(extra_meta)
            return df, meta

        except Exception as e:
            err_msg = str(e)
            logger.error(f"Online retrieval failed for {self.name}: {err_msg}")
            self._save_metadata(record_count=0, success=False, error_msg=err_msg)

            # Fallback to existing cache if available
            if self.cache_path.exists():
                try:
                    df = self.load_from_cache()
                    self.is_cached = True
                    meta = self.get_provenance(len(df))
                    meta["freshness_type"] = "Cached (Fallback after network failure)"
                    meta["warning"] = f"Online refresh failed: {err_msg}. Showing historical cached records."
                    return df, meta
                except Exception as cache_err:
                    logger.error(f"Cache fallback also failed: {cache_err}")

            # Re-raise if no cache available
            meta = self.get_provenance(0)
            meta["freshness_type"] = "Unavailable"
            meta["error"] = err_msg
            return pd.DataFrame(), meta

    def save_to_cache(self, df: pd.DataFrame):
        """Saves dataframe to disk in CSV format."""
        df.to_csv(self.cache_path, index=False, encoding="utf-8")

    def load_from_cache(self) -> pd.DataFrame:
        """Loads dataframe from disk cache."""
        return pd.read_csv(self.cache_path, encoding="utf-8")

    def get_provenance(self, record_count: int) -> Dict[str, Any]:
        """Returns standard provenance metadata for scientific traceability."""
        now = datetime.now(timezone.utc)
        age_str = "N/A"
        if self.last_retrieval_time:
            diff_secs = (now - self.last_retrieval_time).total_seconds()
            if diff_secs < 60:
                age_str = f"{int(diff_secs)}s ago"
            elif diff_secs < 3600:
                age_str = f"{int(diff_secs // 60)}m ago"
            else:
                age_str = f"{diff_secs / 3600:.1f}h ago"

        return {
            "source_name": self.name,
            "source_url": self.source_url,
            "retrieval_time": self.last_retrieval_time.isoformat() if self.last_retrieval_time else None,
            "data_age": age_str,
            "record_count": record_count,
            "is_cached": self.is_cached,
            "status": self.last_status,
            "last_error": self.last_error
        }

    @abstractmethod
    def describe_capabilities(self) -> Dict[str, Any]:
        """Provides human-readable description of measurements, units, and limitations."""
        pass
