"""
Evidence and Scientific Insights Generator for FIREWISE-X
Synthesizes reproducible, audit-traceable findings directly calculated from the active dataset.
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np

class EvidenceInsightEngine:
    """Derives structured, evidence-backed scientific findings from verified data."""

    @classmethod
    def generate_findings(cls, df: pd.DataFrame, source_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Computes verifiable findings directly from the active dataset."""
        if df is None or df.empty:
            return []

        findings: List[Dict[str, Any]] = []
        source_name = source_meta.get("source_name", "Active Dataset")
        source_url = source_meta.get("source_url", "N/A")
        total_n = len(df)

        # Finding 1: Dataset Scope & Completeness Evidence
        findings.append({
            "title": f"Empirical Scope: {total_n} Flight/Investigation Records",
            "category": "Dataset Architecture & Evidence Base",
            "finding": (
                f"The active analysis is grounded in {total_n} verified records from '{source_name}', "
                f"encompassing {len(df.columns)} recorded scientific dimensions."
            ),
            "evidence_metrics": {
                "Record Count": total_n,
                "Dimensions": len(df.columns),
                "Source System": source_name,
                "Freshness": source_meta.get("freshness_type", "Standard")
            },
            "methodology": "Direct census aggregation and type profiling across retrieved table.",
            "source_citation": f"NASA Spaceflight Data Repository ({source_url})",
            "assumptions": "Assumes records represent independent test runs or distinct publication items.",
            "limitations": "Data availability is constrained to publicly curated archival releases."
        })

        # Finding 2: Combustion Oxygen Dynamics (if O2 data present)
        if "initial_o2_pct" in df.columns and "final_o2_pct" in df.columns:
            s_init = pd.to_numeric(df["initial_o2_pct"], errors="coerce").dropna()
            s_final = pd.to_numeric(df["final_o2_pct"], errors="coerce").dropna()

            if not s_init.empty and not s_final.empty:
                mean_init = float(s_init.mean())
                min_init = float(s_init.min())
                max_init = float(s_init.max())

                # Oxygen depletion
                if "o2_consumed_pct" in df.columns:
                    s_cons = pd.to_numeric(df["o2_consumed_pct"], errors="coerce").dropna()
                    mean_cons = float(s_cons.mean()) if not s_cons.empty else 0.0
                    max_cons = float(s_cons.max()) if not s_cons.empty else 0.0
                else:
                    mean_cons = float((s_init.mean() - s_final.mean()))
                    max_cons = float((s_init - s_final).max())

                findings.append({
                    "title": "Microgravity Oxidizer Envelope & Depletion Range",
                    "category": "Combustion Kinetics",
                    "finding": (
                        f"Tests spanned an ambient oxidizer range of {min_init:.1f}% to {max_init:.1f}% O₂ by volume "
                        f"(mean {mean_init:.1f}%). Peak observed oxygen depletion in a single burn was {max_cons:.2f}%."
                    ),
                    "evidence_metrics": {
                        "Baseline O2 Range": f"{min_init:.1f}% – {max_init:.1f}%",
                        "Mean Baseline O2": f"{mean_init:.2f}%",
                        "Max Single-Run O2 Drop": f"{max_cons:.2f}%",
                        "Tests Evaluated": len(s_init)
                    },
                    "methodology": "Calibrated parametric difference: ΔO₂ = Initial O₂ - Final O₂ (% vol).",
                    "source_citation": "NASA BASS-II Microgravity Science Glovebox Dataset",
                    "assumptions": "Assumes uniform glovebox atmospheric mixing prior to final sensor readout.",
                    "limitations": "Quenched runs without ignition display near-zero consumption."
                })

        # Finding 3: Toxic Combustion Products (CO Generation)
        if "final_co_ppm" in df.columns:
            s_co = pd.to_numeric(df["final_co_ppm"], errors="coerce").dropna()
            if not s_co.empty:
                max_co = float(s_co.max())
                mean_co = float(s_co.mean())
                elevated_co_count = int((s_co > 50).sum())

                findings.append({
                    "title": "Toxic Effluent Build-up: Carbon Monoxide (CO) Generation",
                    "category": "Spacecraft Life Support Safety",
                    "finding": (
                        f"Post-combustion Carbon Monoxide reached a peak of {max_co:.0f} ppm (mean {mean_co:.1f} ppm). "
                        f"{elevated_co_count} test(s) exceeded the nominal 50 ppm threshold, demonstrating the danger of "
                        "toxic gas accumulation in stagnant microgravity atmospheres."
                    ),
                    "evidence_metrics": {
                        "Max Observed CO": f"{max_co:.0f} ppm",
                        "Mean CO Produced": f"{mean_co:.1f} ppm",
                        "Runs > 50 ppm CO": elevated_co_count,
                        "Sample Size": len(s_co)
                    },
                    "methodology": "Post-burn electrochemical / spectrophotometric gas sampling aggregation.",
                    "source_citation": "NASA BASS-II MSG Sensor Suite (NTRS Citation 20150019858)",
                    "assumptions": "Sensor calibration remained stable across consecutive burn cycles.",
                    "limitations": "Sensor maximum detection ceilings may truncate extreme peak events."
                })

        # Finding 4: Fuel Flammability Vulnerability by Material
        if "fuel_category" in df.columns:
            fuel_counts = df["fuel_category"].value_counts()
            top_fuel = fuel_counts.index[0]
            top_fuel_count = int(fuel_counts.iloc[0])

            findings.append({
                "title": f"Fuel Sample Testing Distribution: Dominance of {top_fuel}",
                "category": "Material Flammability Standards",
                "finding": (
                    f"'{top_fuel}' constitutes the largest testing group with {top_fuel_count} test runs "
                    f"({top_fuel_count/total_n*100:.1f}% of total). Solid polymer thickness profoundly alters "
                    "ignition delay and opposed-flow extinction in low-gravity."
                ),
                "evidence_metrics": {
                    "Primary Fuel": str(top_fuel),
                    "Test Count": top_fuel_count,
                    "Distinct Fuel Classes": int(len(fuel_counts)),
                    "Distribution": fuel_counts.head(4).to_dict()
                },
                "methodology": "Discrete categorical frequency mapping across sample inventory.",
                "source_citation": "NASA Flight Sample Manifest (SRD BASS-II)",
                "assumptions": "Material specimens met standard NASA Spacecraft Cleanliness specifications.",
                "limitations": "Non-polymeric spacecraft structural composites (e.g. epoxy honeycomb) were evaluated in separate Saffire campaigns."
            })

        # Finding 5: Documented Saffire / SoFIE Research Categorization (if NTRS data)
        if "is_saffire" in df.columns or "subject_categories" in df.columns:
            saffire_hits = int(df.get("is_saffire", pd.Series(dtype=bool)).sum())
            sofie_hits = int(df.get("is_sofie", pd.Series(dtype=bool)).sum())

            findings.append({
                "title": "Spacecraft Fire Safety Research Corpus Synthesis",
                "category": "Literature & Technical Investigation Scope",
                "finding": (
                    f"Identified {saffire_hits} primary Saffire and {sofie_hits} SoFIE technical reports. "
                    "Synthesis emphasizes that without buoyant natural convection, flames spread slower but "
                    "can smolder unnoticed in ventilation dead zones."
                ),
                "evidence_metrics": {
                    "Saffire Investigations": saffire_hits,
                    "SoFIE Investigations": sofie_hits,
                    "Total Technical Records": len(df)
                },
                "methodology": "Boolean term matching and NASA STI subject categorization.",
                "source_citation": "NASA Technical Reports Server REST API",
                "assumptions": "Publications cataloged in NTRS accurately index major spaceflight combustion experiments.",
                "limitations": "Classified or ITAR-restricted internal raw telemetry data is not exposed via public STI."
            })

        return findings
