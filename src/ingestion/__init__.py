from src.ingestion.base import BaseDataConnector
from src.ingestion.nasa_bass import NASABass2Connector
from src.ingestion.nasa_ntrs import NASANtrsConnector
from src.ingestion.nasa_saffire import NASASaffireConnector
from src.ingestion.nasa_sofie import NASASofieConnector
from src.ingestion.generic_http import GenericHttpConnector

AVAILABLE_CONNECTORS = {
    "nasa_bass2": NASABass2Connector,
    "nasa_ntrs": NASANtrsConnector,
    "nasa_saffire": NASASaffireConnector,
    "nasa_sofie": NASASofieConnector,
    "generic_http": GenericHttpConnector
}

__all__ = [
    "BaseDataConnector",
    "NASABass2Connector",
    "NASANtrsConnector",
    "NASASaffireConnector",
    "NASASofieConnector",
    "GenericHttpConnector",
    "AVAILABLE_CONNECTORS"
]
