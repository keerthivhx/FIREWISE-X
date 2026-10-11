"""
Trend, Correlation, and Group-Level Analysis for FIREWISE-X
Analyzes scientific relationships across microgravity combustion parameters.
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

class TrendAnalyzer:
    """Computes correlation matrices, group comparisons, and trends across conditions."""

    @classmethod
    def compute_correlations(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates Pearson and Spearman correlation matrices for numeric features."""
        numeric_df = df.select_dtypes(include=[np.number]).dropna(how="all", axis=1)

        # Require at least 2 numeric columns and 3 non-empty rows
        if numeric_df.shape[1] < 2 or len(numeric_df.dropna()) < 3:
            return {
                "has_correlations": False,
                "reason": "Insufficient numeric features or observations for correlation matrix."
            }

        # Drop columns with zero variance
        valid_cols = [c for c in numeric_df.columns if numeric_df[c].std() > 1e-9]
        if len(valid_cols) < 2:
            return {
                "has_correlations": False,
                "reason": "Numeric columns lack sufficient variance."
            }

        corr_pearson = numeric_df[valid_cols].corr(method="pearson").round(3)
        corr_spearman = numeric_df[valid_cols].corr(method="spearman").round(3)

        # Extract strongest relationships
        pairs = []
        for i in range(len(valid_cols)):
            for j in range(i + 1, len(valid_cols)):
                c1, c2 = valid_cols[i], valid_cols[j]
                val = corr_pearson.loc[c1, c2]
                if pd.notna(val):
                    pairs.append({
                        "var1": c1,
                        "var2": c2,
                        "pearson_r": float(val),
                        "abs_r": abs(float(val))
                    })

        pairs = sorted(pairs, key=lambda x: x["abs_r"], reverse=True)

        return {
            "has_correlations": True,
            "columns": valid_cols,
            "pearson_matrix": corr_pearson.to_dict(),
            "spearman_matrix": corr_spearman.to_dict(),
            "top_correlations": pairs[:8]
        }

    @classmethod
    def analyze_by_group(cls, df: pd.DataFrame, group_col: str, metric_cols: Optional[list] = None) -> Dict[str, Any]:
        """Groups data by a categorical feature and computes comparative statistics."""
        if group_col not in df.columns:
            return {"valid": False, "reason": f"Column '{group_col}' not found."}

        num_df = df.select_dtypes(include=[np.number])
        if metric_cols is None:
            metric_cols = [c for c in num_df.columns if not c.startswith("_")][:5]

        if not metric_cols:
            return {"valid": False, "reason": "No numeric metric columns available for grouping."}

        grouped = df.groupby(group_col)[metric_cols].agg(["count", "mean", "median", "std"]).round(3)

        # Convert multi-level column names for clean visualization
        flat_records = []
        for grp_name, sub in df.groupby(group_col):
            record = {"group": str(grp_name), "count": len(sub)}
            for m in metric_cols:
                s = sub[m].dropna()
                record[f"{m}_mean"] = round(float(s.mean()), 3) if not s.empty else None
                record[f"{m}_median"] = round(float(s.median()), 3) if not s.empty else None
            flat_records.append(record)

        return {
            "valid": True,
            "group_column": group_col,
            "metric_columns": metric_cols,
            "summary_table": flat_records
        }
