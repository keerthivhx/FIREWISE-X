"""
FIREWISE-X Configuration Module
Centralized settings for data sources, cache paths, validation limits, and UI styling.
"""

from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
DEMO_DIR = DATA_DIR / "demo"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DIR.mkdir(parents=True, exist_ok=True)

# Network Configuration
DEFAULT_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "15"))
DEFAULT_RETRIES = 3
DEFAULT_CACHE_TTL = int(os.environ.get("CACHE_TTL_SECONDS", "3600"))  # 1 hour
USER_AGENT = "FIREWISE-X/1.0 (NASA Space Apps Challenge 2026; Microgravity Fire Safety Research)"

# Verified Online Data Sources
ENDPOINTS = {
    "NASA_NTRS_SEARCH": "https://ntrs.nasa.gov/api/citations/search",
    "NASA_BASS2_DATASET": "https://raw.githubusercontent.com/Sufia90/FireGuard-AI/main/data/experiments/bass2_experimental_table.csv",
    "NASA_METADATA_LINKS": "https://raw.githubusercontent.com/Sufia90/FireGuard-AI/main/data/metadata/nasa_links.csv",
    "NASA_PSI_PORTAL": "https://psi.nasa.gov",
    "NASA_SAFFIRE_INFO": "https://gipoc.grc.nasa.gov/wp/other-iss/saffire/",
    "NASA_SOFIE_INFO": "https://science.nasa.gov/biological-physical/investigations/sofie/",
}

# Physical bounds for validation of combustion measurements
PHYSICAL_BOUNDS = {
    "o2_pct": {"min": 0.0, "max": 100.0, "unit": "% by volume", "label": "Oxygen Concentration"},
    "co2_pct": {"min": 0.0, "max": 100.0, "unit": "% by volume", "label": "Carbon Dioxide Concentration"},
    "co_ppm": {"min": 0.0, "max": 50000.0, "unit": "ppm", "label": "Carbon Monoxide"},
    "flow_restrictor": {"min": 0.0, "max": 10.0, "unit": "setting", "label": "Flow Restrictor Index"},
    "fan_display": {"min": 0.0, "max": 200.0, "unit": "setting", "label": "Fan Speed Display"},
    "air_display": {"min": 0.0, "max": 50.0, "unit": "setting", "label": "Air Flow Display"},
    "radiometer_gain": {"valid_set": {10, 50, 250, 1000}, "unit": "gain", "label": "Radiometer Gain"},
}

# UI Styling Constants (Dark navy & deep space aesthetic)
THEME_COLORS = {
    "background": "#0b1021",
    "surface": "#121a36",
    "surface_accent": "#1a254d",
    "primary": "#00d2ff",
    "primary_dark": "#0083b0",
    "accent_orange": "#ff6b4a",
    "accent_yellow": "#f7b731",
    "accent_green": "#20bf6b",
    "text": "#e0e6ed",
    "text_muted": "#8d99ae",
    "border": "#23315a"
}
