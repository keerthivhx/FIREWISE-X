"""
Descriptive Statistics and Dynamic Dataset Summarization for FIREWISE-X
Adapts dynamically to the fields actually present in the active dataset.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

class DescriptiveAnalyzer:
    """Computes dynamic, reproducible descriptive statistics on active scientific datasets."""

    @classmethod
    def analyze(cls, df: pd.DataFrame) -> Dict[str, Any]:
        if df is None or df.empty:
            return {
                "record_count": 0,
                "numeric_metrics": {},
                "categorical_summaries": {},
                "summary_text": "Dataset is empty."
            }

        numeric_df = df.select_dtypes(include=[np.number])
        cat_df = df.select_dtypes(include=["object", "category"])

        # 1. Numeric statistics
        num_stats = {}
        for col in numeric_df.columns:
            s = numeric_df[col].dropna()
            if not s.empty:
                q25 = float(s.quantile(0.25))
                q75 = float(s.quantile(0.75))
                num_stats[col] = {
                    "count": int(s.count()),
                    "mean": round(float(s.mean()), 3),
                    "std": round(float(s.std()), 3) if len(s) > 1 else 0.0,
                    "min": round(float(s.min()), 3),
                    "q25": round(q25, 3),
                    "median": round(float(s.median()), 3),
                    "q75": round(q75, 3),
                    "max": round(float(s.max()), 3),
                    "iqr": round(q75 - q25, 3),
                    "missing": int(numeric_df[col].isna().sum())
                }

        # 2. Categorical statistics
        cat_stats = {}
        for col in cat_df.columns:
            s = cat_df[col].dropna()
            if not s.empty:
                counts = s.value_counts()
                top_items = counts.head(5).to_dict()
                cat_stats[col] = {
                    "unique_count": int(s.nunique()),
                    "top_values": top_items,
                    "mode": str(counts.index[0]) if not counts.empty else "N/A",
                    "mode_freq": int(counts.iloc[0]) if not counts.empty else 0
                }

        return {
            "record_count": len(df),
            "column_count": len(df.columns),
            "numeric_metrics": num_stats,
            "categorical_summaries": cat_stats,
            "summary_text": (
                f"Dataset contains {len(df)} records across {len(df.columns)} dimensions "
                f"({len(num_stats)} numeric, {len(cat_stats)} categorical)."
            )
        }
