"""
Reproducible Data Cleaning and Transformation Module for FIREWISE-X
Prepares scientific datasets for analysis while maintaining an audit log of all transformations.
"""

from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np

class ScientificDataCleaner:
    """Performs transparent, auditable cleaning on retrieved datasets."""

    @classmethod
    def clean(cls, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Cleans dataframe non-destructively:
        - Coerces numeric columns while leaving originals intact or safely typed
        - Strips whitespace
        - Computes derived physical combustion variables if corresponding fields exist
        - Returns (cleaned_df, transformation_log)
        """
        if df_raw is None or df_raw.empty:
            return pd.DataFrame(), ["Dataset is empty. No operations performed."]

        df = df_raw.copy()
        log: List[str] = []

        # 1. Clean string fields
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()
            # Replace string 'nan', 'none', 'null' with NaN
            df[col] = df[col].replace(["nan", "None", "null", "NaN", ""], np.nan)

        log.append("Normalized string representations and standardized blank cells.")

        # 2. Coerce numeric columns where appropriate
        numeric_candidates = [
            "flow_restrictor", "fan_display", "air_display", "radiometer_gain",
            "total_frames", "initial_o2_pct", "final_o2_pct",
            "initial_co2_pct", "final_co2_pct", "initial_co_ppm", "final_co_ppm"
        ]

        coerced_count = 0
        for col in df.columns:
            # Check if candidate or column looks predominantly numeric
            if col in numeric_candidates or any(k in col.lower() for k in ["pct", "ppm", "frames", "display", "gain"]):
                s_num = pd.to_numeric(df[col], errors="coerce")
                if s_num.notna().sum() > 0:
                    df[col] = s_num
                    coerced_count += 1

        if coerced_count > 0:
            log.append(f"Parsed and coerced {coerced_count} columns to standard IEEE-754 floating-point format.")

        # 3. Derive microgravity combustion kinetics if BASS-II or similar fields exist
        if "initial_o2_pct" in df.columns and "final_o2_pct" in df.columns:
            # Delta O2 (consumption is negative delta)
            df["delta_o2_pct"] = df["final_o2_pct"] - df["initial_o2_pct"]
            df["o2_consumed_pct"] = df["initial_o2_pct"] - df["final_o2_pct"]
            log.append("Computed Oxygen Consumption: ΔO₂ = Final O₂ - Initial O₂ (% vol).")

        if "initial_co2_pct" in df.columns and "final_co2_pct" in df.columns:
            df["delta_co2_pct"] = df["final_co2_pct"] - df["initial_co2_pct"]
            log.append("Computed Carbon Dioxide Generation: ΔCO₂ = Final CO₂ - Initial CO₂ (% vol).")

        if "initial_co_ppm" in df.columns and "final_co_ppm" in df.columns:
            df["delta_co_ppm"] = df["final_co_ppm"] - df["initial_co_ppm"]
            log.append("Computed Carbon Monoxide Generation: ΔCO = Final CO - Initial CO (ppm).")

        # Flammability / Burn event classification based on physical measurements
        if "delta_co2_pct" in df.columns and "delta_co_ppm" in df.columns:
            def classify_burn(row):
                d_co2 = row.get("delta_co2_pct")
                d_co = row.get("delta_co_ppm")
                frames = row.get("total_frames", 0)

                # If CO2 increased or CO increased significantly or frames shot > 0
                has_effluent = (pd.notna(d_co2) and d_co2 > 0.05) or (pd.notna(d_co) and d_co > 5.0)
                has_frames = pd.notna(frames) and frames > 0

                if has_effluent or has_frames:
                    return "Sustained Burn"
                elif pd.isna(d_co2) and pd.isna(d_co) and pd.isna(frames):
                    return "Incomplete / Untested"
                else:
                    return "Extinguished / Suppressed"

            df["combustion_outcome"] = df.apply(classify_burn, axis=1)
            log.append("Classified physical combustion outcome into Sustained Burn vs. Extinguished/Suppressed.")

        return df, log
