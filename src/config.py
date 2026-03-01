# src/config.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

config = load_config()

def get_latest_version(api_class: str) -> str:
    """Returns the configured latest version for a given API class."""
    latest_versions = config.get("api_docs", {}).get("latest_versions", {})
    return latest_versions.get(api_class.upper())

def get_file_mappings() -> list:
    """Returns the list of files and their explicit metadata."""
    return config.get("api_docs", {}).get("files", [])