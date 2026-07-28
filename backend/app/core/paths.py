# app/core/paths.py

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FLOW_DIR = ROOT / "flows"
PROFILE_DIR = ROOT / "profiles"
DATA_DIR = ROOT / "data"