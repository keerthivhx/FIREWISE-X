"""
Unit Tests for Scientific Analysis & Machine Learning Engines
"""

import pandas as pd
import numpy as np
from src.analysis.descriptive import DescriptiveAnalyzer
from src.analysis.trends import TrendAnalyzer
from src.analysis.anomalies import StatisticalAnomalyDetector
from src.ml.models import MicrogravityMLEngine

def test_descriptive_statistics_accuracy():
    df = pd.DataFrame({"o2": [10.0, 20.0, 30.0, 40.0, 50.0]})
    res = DescriptiveAnalyzer.analyze(df)
    m = res["numeric_metrics"]["o2"]
    assert m["count"] == 5
    assert m["mean"] == 30.0
    assert m["median"] == 30.0
    assert m["min"] == 10.0
    assert m["max"] == 50.0
    assert m["iqr"] == 20.0


def test_different_datasets_produce_different_results():
    """Validates the strict non-hardcoded requirement."""
    df1 = pd.DataFrame({"o2": [15.0, 16.0, 17.0]})
    df2 = pd.DataFrame({"o2": [25.0, 30.0, 35.0]})

    res1 = DescriptiveAnalyzer.analyze(df1)
    res2 = DescriptiveAnalyzer.analyze(df2)

    assert res1["numeric_metrics"]["o2"]["mean"] != res2["numeric_metrics"]["o2"]["mean"]
    assert res1["numeric_metrics"]["o2"]["max"] != res2["numeric_metrics"]["o2"]["max"]


def test_trend_correlation_matrix():
    df = pd.DataFrame({
        "flow": [1.0, 2.0, 3.0, 4.0, 5.0],
        "flame_temp": [500.0, 600.0, 700.0, 800.0, 900.0]
    })
    res = TrendAnalyzer.compute_correlations(df)
    assert res["has_correlations"] is True
    # Perfect linear relationship: r should be 1.0
    assert res["pearson_matrix"]["flow"]["flame_temp"] == 1.0


def test_iqr_outlier_detection():
    # 10 nominal points and 1 extreme outlier
    df = pd.DataFrame({
        "co_ppm": [10.0, 11.0, 10.5, 9.8, 10.2, 10.1, 9.9, 10.4, 10.0, 10.2, 500.0]
    })
    res = StatisticalAnomalyDetector.detect_univariate_outliers(df, "co_ppm")
    assert res["valid"] is True
    assert res["outlier_count"] == 1
    assert res["outliers"][0]["value"] == 500.0


def test_ml_isolation_forest_guardrails():
    # Insufficient data (< 10 samples) should be rejected
    small_df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    res_small = MicrogravityMLEngine.run_isolation_forest(small_df)
    assert res_small["trained"] is False
    assert "Insufficient" in res_small["reason"]

    # Sufficient samples (e.g. 25 samples) should successfully train
    np.random.seed(42)
    norm_data = np.random.normal(loc=20.0, scale=2.0, size=(30, 3))
    good_df = pd.DataFrame(norm_data, columns=["feat_a", "feat_b", "feat_c"])
    res_good = MicrogravityMLEngine.run_isolation_forest(good_df, contamination=0.1)
    assert res_good["trained"] is True
    assert res_good["anomaly_count"] > 0
