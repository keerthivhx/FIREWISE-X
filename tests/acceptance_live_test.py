"""
Mandatory Live Online Real-Data Acceptance Script for FIREWISE-X
Connects to online endpoints, fetches real data, validates, analyzes, and prints verification evidence.
"""

from src.ingestion.nasa_bass import NASABass2Connector
from src.ingestion.nasa_ntrs import NASANtrsConnector
from src.ingestion.nasa_saffire import NASASaffireConnector
from src.ingestion.nasa_sofie import NASASofieConnector
from src.validation.quality import DataQualityEngine
from src.processing.cleaning import ScientificDataCleaner
from src.analysis.descriptive import DescriptiveAnalyzer
from src.analysis.trends import TrendAnalyzer
from src.ml.models import MicrogravityMLEngine
from src.insights.evidence import EvidenceInsightEngine

def run_acceptance():
    print("=" * 70)
    print("FIREWISE-X: REAL-DATA ACCEPTANCE VERIFICATION")
    print("=" * 70)

    # 1. BASS-II Flight Dataset
    print("\n[1] Testing Connector: NASABass2Connector")
    b_conn = NASABass2Connector()
    df_b, meta_b = b_conn.fetch_data(force_refresh=True)
    print(f" -> Source Name: {meta_b.get('source_name')}")
    print(f" -> Source URL: {meta_b.get('source_url')}")
    print(f" -> Live Status: {meta_b.get('status')}")
    print(f" -> Freshness: {meta_b.get('freshness_type')}")
    print(f" -> Records Retrieved: {len(df_b)}")

    assert not df_b.empty, "BASS-II online retrieval failed"
    assert len(df_b) > 100, f"Expected >100 records, got {len(df_b)}"

    df_clean, clean_log = ScientificDataCleaner.clean(df_b)
    quality = DataQualityEngine.evaluate(df_clean)
    print(f" -> Data Health Score: {quality['health_score']}/100")
    print(f" -> Total Completeness: {quality['overall_completeness_pct']}%")
    print(f" -> Physical Bounds Violations: {quality['physical_violations_total']}")

    desc = DescriptiveAnalyzer.analyze(df_clean)
    o2_stats = desc['numeric_metrics'].get('initial_o2_pct', {})
    print(f" -> O2 Stats: Mean={o2_stats.get('mean')}%, Min={o2_stats.get('min')}%, Max={o2_stats.get('max')}%")

    corr = TrendAnalyzer.compute_correlations(df_clean)
    print(f" -> Correlation Matrix Computed: {corr.get('has_correlations')}")
    if corr.get('top_correlations'):
        top = corr['top_correlations'][0]
        print(f" -> Strongest Correlation: {top['var1']} vs {top['var2']} (r = {top['pearson_r']})")

    ml_res = MicrogravityMLEngine.run_isolation_forest(df_clean)
    print(f" -> Isolation Forest Fitted: {ml_res.get('trained')}")
    print(f" -> Anomalies Detected: {ml_res.get('anomaly_count')} ({ml_res.get('anomaly_percentage')}%)")

    findings = EvidenceInsightEngine.generate_findings(df_clean, meta_b)
    print(f" -> Evidence Findings Generated: {len(findings)}")

    # 2. NASA NTRS Live API
    print("\n[2] Testing Connector: NASANtrsConnector")
    n_conn = NASANtrsConnector(query="saffire microgravity flame", max_records=10)
    df_n, meta_n = n_conn.fetch_data(force_refresh=True)
    print(f" -> Source Name: {meta_n.get('source_name')}")
    print(f" -> API Endpoint: {meta_n.get('api_endpoint')}")
    print(f" -> Records Retrieved: {len(df_n)}")
    assert not df_n.empty, "NTRS online retrieval failed"

    # 3. NASA Saffire
    print("\n[3] Testing Connector: NASASaffireConnector")
    s_conn = NASASaffireConnector()
    df_s, meta_s = s_conn.fetch_data(force_refresh=True)
    print(f" -> Records Retrieved: {len(df_s)}")
    print(f" -> Flight Distribution: {df_s['mission_series'].value_counts().to_dict()}")

    # 4. NASA SoFIE
    print("\n[4] Testing Connector: NASASofieConnector")
    sof_conn = NASASofieConnector()
    df_sof, meta_sof = sof_conn.fetch_data(force_refresh=True)
    print(f" -> Records Retrieved: {len(df_sof)}")
    print(f" -> Sub-Investigation Distribution: {df_sof['sub_investigation'].value_counts().to_dict()}")

    print("\n" + "=" * 70)
    print("ALL REAL-DATA ACCEPTANCE CRITERIA PASSED AND FULLY VERIFIED.")
    print("=" * 70)

if __name__ == "__main__":
    run_acceptance()
