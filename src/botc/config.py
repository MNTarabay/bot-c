import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _path(var, default):
    v = os.environ.get(var)
    return Path(v) if v else default


DATA_DIR = _path("BOTC_DATA_DIR", ROOT / "data")
LOG_FILE = _path("BOTC_LOG_FILE", DATA_DIR / "botc.log")
PARAMS_FILE = _path("BOTC_PARAMS", ROOT / "config" / "params.yaml")

with open(PARAMS_FILE) as f:
    P = yaml.safe_load(f)
