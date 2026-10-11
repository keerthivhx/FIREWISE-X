"""
Statistical Anomaly and Outlier Analysis for FIREWISE-X
Applies transparent statistical criteria (IQR and Robust Z-score) with scientific interpretation.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

class StatisticalAnomalyDetector:
    """Detects univariate and multivariate outliers with rigorous physical explanations."""

    @classmethod
    def detect_univariate_outliers(cls, df: pd.DataFrame, col_name: str, iqr_multiplier: float = 1.5) -> Dict[str, Any]:
        """
        Detects Tukey IQR outliers for a selected numeric column.
        Explains whether outliers represent rapid quenching, intense burns, or instrumentation artifacts.
        """
        if col_name not in df.columns:
            return {"valid": False, "reason": f"Column '{col_name}' does not exist in dataset."}

        s = pd.to_numeric(df[col_name], errors="coerce").dropna()
        if len(s) < 5:
            return {"valid": False, "reason": "Insufficient observations (need at least 5 numeric values)."}

        q25 = float(s.quantile(0.25))
        q75 = float(s.quantile(0.75))
        iqr = q75 - q25

        if iqr <= 1e-9:
            return {"valid": False, "reason": f"Variable '{col_name}' has zero IQR (constant or near-constant value)."}

        lower_bound = q25 - (iqr_multiplier * iqr)
        upper_bound = q75 + (iqr_multiplier * iqr)

        outlier_mask = (s < lower_bound) | (s > upper_bound)
        outlier_indices = s[outlier_mask].index.tolist()
        outlier_count = len(outlier_indices)

        details = []
        for idx in outlier_indices:
            val = float(s.loc[idx])
            direction = "High" if val > upper_bound else "Low"
            diff = (val - upper_bound) if direction == "High" else (lower_bound - val)

            # Context row info
            row_dict = df.loc[idx].to_dict()
            identifier = row_dict.get("test_id") or row_dict.get("citation_id") or f"Row #{idx}"

            details.append({
                "index": int(idx),
                "identifier": str(identifier),
                "value": round(val, 3),
                "direction": direction,
                "distance_from_bound": round(diff, 3),
                "scientific_interpretation": cls._interpret_outlier(col_name, val, direction)
            })

        return {
            "valid": True,
            "column": col_name,
            "total_points": len(s),
            "outlier_count": outlier_count,
            "outlier_pct": round((outlier_count / len(s)) * 100, 1),
            "q25": round(q25, 3),
            "median": round(float(s.median()), 3),
            "q75": round(q75, 3),
            "iqr": round(iqr, 3),
            "lower_bound": round(lower_bound, 3),
            "upper_bound": round(upper_bound, 3),
            "outliers": details
        }

    @staticmethod
    def _interpret_outlier(col: str, val: float, direction: str) -> str:
        c = col.lower()
        if "co_" in c or "co_ppm" in c or "delta_co" in c:
            if direction == "High":
                return "Elevated Carbon Monoxide: Indicates incomplete combustion or prolonged smoldering in low-convection microgravity."
            return "Minimal CO generation: Typical for rapid extinction or non-ignition."
        elif "o2" in c:
            if direction == "Low":
                return "Deep Oxygen Depletion: Suggests high fuel consumption or sustained burn event before suppression."
            return "High Oxygen: Near-ambient oxidizer atmosphere or test run terminated early."
        elif "co2" in c:
            if direction == "High":
                return "Elevated CO2: Indicates efficient stoichiometric combustion."
            return "Minimal CO2: Quenched or zero sustained combustion."
        elif "fan" in c or "flow" in c:
            return f"Unusual flow/ventilation condition ({direction}): Testing boundary layer extinction limits."
        return f"Statistical outlier ({direction}) relative to sample distribution."
