import json
import time

import numpy as np

from botc.config import DATA_DIR, P

U = P["universe"]
STABLE = set(U["stablecoins"])
UNIVERSE_FILE = DATA_DIR / "universe.json"
MAX_AGE_S = U["max_age_days"] * 86400
TOP_N = U["top_n"]
FLOOR_USD = U["floor_usd"]


def build_universe(client):
    pairs = client.asset_pairs()
    usd = [cd for cd, i in pairs.items()
           if i.get("wsname", "").endswith("/USD")
           and ".d" not in cd
           and i["wsname"].split("/")[0] not in STABLE]
    scored = []
    for p in usd:
        try:
            raw = client.get_ohlc(p, interval=1440)
            if len(raw) < U["min_history_bars"]:
                continue
            dv = [float(r[4]) * float(r[6]) for r in raw[-30:]]
            med = float(np.median(dv))
            if med >= FLOOR_USD:
                scored.append((med, p))
            time.sleep(P["api"]["request_pause_s"])
        except Exception:
            continue
    scored.sort(reverse=True)
    uni = [p for _, p in scored[:TOP_N]]
    json.dump({"built": int(time.time()), "pairs": uni,
               "median_vols": {p: round(m) for m, p in scored[:TOP_N]}},
              open(UNIVERSE_FILE, "w"), indent=2)
    return uni


def get_universe(client):
    try:
        d = json.load(open(UNIVERSE_FILE))
        if time.time() - d["built"] < MAX_AGE_S:
            return d["pairs"]
    except Exception:
        pass
    return build_universe(client)
