"""
Scientific Data Quality Assessment Module for FIREWISE-X
Performs comprehensive validation without silently discarding valid scientific observations.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from src.config import PHYSICAL_BOUNDS

class DataQualityEngine:
    """Scientific validation suite inspecting dataset health, types, completeness, and physical bounds."""

    @classmethod
    def evaluate(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """Runs a complete scientific data quality audit on the dataframe."""
        if df is None or df.empty:
            return {
                "is_empty": True,
                "record_count": 0,
                "column_count": 0,
                "health_score": 0.0,
                "issues": ["Dataset is empty."],
                "column_profiles": {},
                "summary": "No data available."
            }

        total_rows = len(df)
        total_cols = len(df.columns)
        issues: List[str] = []

        # 1. Duplicates
        duplicate_count = int(df.duplicated().sum())
        if duplicate_count > 0:
            issues.append(f"Found {duplicate_count} duplicate record(s) ({duplicate_count/total_rows*100:.1f}%).")

        # 2. Column-by-column profiling
        col_profiles = {}
        total_missing = 0
        total_cells = total_rows * total_cols
        physical_violations_total = 0

        for col in df.columns:
            s = df[col]
            missing_count = int(s.isna().sum()) + int((s == "").sum())
            total_missing += missing_count
            missing_pct = (missing_count / total_rows) * 100.0

            # Detect data type
            numeric_series = pd.to_numeric(s, errors="coerce")
            is_numeric = numeric_series.notna().sum() > (total_rows * 0.5)

            profile: Dict[str, Any] = {
                "inferred_type": "Numeric" if is_numeric else "Categorical / Text",
                "missing_count": missing_count,
                "missing_pct": round(missing_pct, 1),
                "unique_values": int(s.nunique(dropna=True)),
                "sample_values": [str(v) for v in s.dropna().unique()[:4]]
            }

            # Check numeric stats and physical bounds if applicable
            if is_numeric:
                valid_num = numeric_series.dropna()
                if not valid_num.empty:
                    profile["min"] = float(valid_num.min())
                    profile["max"] = float(valid_num.max())
                    profile["mean"] = round(float(valid_num.mean()), 3)
                    profile["std"] = round(float(valid_num.std()), 3) if len(valid_num) > 1 else 0.0

                    # Check against physical bounds
                    bounds_key = cls._match_bounds_key(col)
                    if bounds_key and bounds_key in PHYSICAL_BOUNDS:
                        rule = PHYSICAL_BOUNDS[bounds_key]
                        violations = 0
                        if "min" in rule:
                            violations += int((valid_num < rule["min"]).sum())
                        if "max" in rule:
                            violations += int((valid_num > rule["max"]).sum())
                        if "valid_set" in rule:
                            violations += int((~valid_num.isin(rule["valid_set"])).sum())

                        profile["physical_rule"] = f"{rule['label']} ({rule.get('unit', '')})"
                        profile["violations"] = violations
                        physical_violations_total += violations
                        if violations > 0:
                            issues.append(f"Column '{col}' has {violations} value(s) outside expected physical bounds.")

            col_profiles[col] = profile

        # Overall health score calculation (0 - 100)
        completeness = max(0.0, 1.0 - (total_missing / max(1, total_cells)))
        uniqueness = max(0.0, 1.0 - (duplicate_count / max(1, total_rows)))
        bounds_integrity = max(0.0, 1.0 - (physical_violations_total / max(1, total_cells)))
        health_score = round((completeness * 0.5 + uniqueness * 0.3 + bounds_integrity * 0.2) * 100, 1)

        return {
            "is_empty": False,
            "record_count": total_rows,
            "column_count": total_cols,
            "duplicate_count": duplicate_count,
            "total_missing_cells": total_missing,
            "overall_completeness_pct": round(completeness * 100, 1),
            "physical_violations_total": physical_violations_total,
            "health_score": health_score,
            "issues": issues,
            "column_profiles": col_profiles,
            "summary": (
                f"{total_rows} records, {total_cols} columns. Data health: {health_score}/100. "
                f"{len(issues)} caution item(s) detected."
            )
        }

    @staticmethod
    def _match_bounds_key(col_name: str) -> str:
        c = col_name.lower().replace(" ", "_")
        if "o2" in c:
            return "o2_pct"
        if "co2" in c:
            return "co2_pct"
        if "co_" in c or "co(" in c or c.endswith("_co") or "co_ppm" in c:
            return "co_ppm"
        if "fan" in c:
            return "fan_display"
        if "air" in c:
            return "air_display"
        if "radiometer" in c or "gain" in c:
            return "radiometer_gain"
        return ""
