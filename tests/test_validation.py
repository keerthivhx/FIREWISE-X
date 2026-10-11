"""
Unit Tests for Data Validation & Quality Assessment
"""

import pandas as pd
import numpy as np
from src.validation.quality import DataQualityEngine

def test_empty_dataset_evaluation():
    empty_df = pd.DataFrame()
    res = DataQualityEngine.evaluate(empty_df)
    assert res["is_empty"] is True
    assert res["health_score"] == 0.0
    assert res["record_count"] == 0


def test_duplicate_and_missing_detection():
    data = pd.DataFrame({
        "sample_id": [1, 1, 2, 3],
        "o2_pct": [21.0, 21.0, np.nan, 20.5],
        "co_ppm": [0.0, 0.0, 50.0, np.nan]
    })
    res = DataQualityEngine.evaluate(data)
    assert res["is_empty"] is False
    assert res["duplicate_count"] == 1
    assert res["total_missing_cells"] == 2
    assert res["health_score"] < 100.0


def test_physical_bounds_violation_detection():
    # Negative oxygen or CO2 > 100% violates physical combustion limits
    data = pd.DataFrame({
        "o2_pct": [-5.0, 21.0, 105.0],
        "co2_pct": [0.04, 150.0, 0.5]
    })
    res = DataQualityEngine.evaluate(data)
    assert res["physical_violations_total"] > 0
    assert any("physical bounds" in issue for issue in res["issues"])
