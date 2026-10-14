"""Bot C daily heartbeat (paper mode only). Runs once after UTC close.
Constitution is law: CONSTITUTION.md governs; this file merely obeys."""
import json
import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from botc.config import DATA_DIR, LOG_FILE, P
from botc.kraken_client import KrakenClient
from botc.universe import get_universe
from botc.gates import entry_gates
from botc.exits import initial_stop, trail_stop

DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler(LOG_FILE)])
log = logging.getLogger("botc")
STATE = DATA_DIR / "state_c.json"
SLOTS = P["portfolio"]["slots"]
ALLOC = P["portfolio"]["alloc"]
PROVE_DAYS = P["exit"]["prove_days"]
PROVE_GAIN = P["exit"]["prove_gain"]
REENTRY_DAYS = P["portfolio"]["reentry_days"]
SLIP = P["portfolio"]["slippage"]
PAUSE = P["api"]["request_pause_s"]


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"equity": P["portfolio"]["start_equity"], "positions": {}, "trade_log": [],
            "last_exit": {}}


def save_state(s):
    json.dump(s, open(STATE, "w"), indent=2)


def buy_ratio_24h(client, pair):
    try:
        since = int((time.time() - 86400) * 1e9)
        res = client.trades(pair, since=since)
        k = next(x for x in res if x != "last")
        tr = res[k]
        if len(tr) < P["entry"]["buy_ratio_min_trades"]:
            return 0.5
        buy = sum(float(t[1]) for t in tr if t[3] == "b")
        tot = sum(float(t[1]) for t in tr)
        return buy / tot if tot > 0 else 0.5
    except Exception:
        return 0.5


def beat():
    client = KrakenClient()
    s = load_state()
    uni = get_universe(client)
    log.info("BEAT start. Equity=%.2f positions=%d universe=%d",
             s["equity"], len(s["positions"]), len(uni))
    today = int(time.time() // 86400)
    for pair in list(s["positions"].keys()):
        pos = s["positions"][pair]
        try:
            raw = client.get_ohlc(pair, interval=1440)
            time.sleep(PAUSE)
        except Exception as e:
            log.error("ohlc %s: %s", pair, e)
            continue
        raw = raw[:-1]
        close = float(raw[-1][4])
        pos["high_water"] = max(pos["high_water"], close)
        gain = pos["high_water"] / pos["entry"] - 1
        pos["stop"] = trail_stop(raw, pos["entry"],
                                 pos["stop"], gain)
        days = today - pos["opened_day"]
        reason = None
        if close <= pos["stop"]:
            reason = "stop"
        elif days >= PROVE_DAYS and gain < PROVE_GAIN:
            reason = "prove_it"
        if reason:
            pnl = (close * (1 - SLIP) - pos["entry"]) * pos["volume"]
            s["equity"] += pnl
            s["trade_log"].append({"ts": int(time.time()),
                "pair": pair, "reason": reason,
                "pnl": round(pnl, 2),
                "peak_gain": round(gain, 4), "days": days,
                "equity": round(s["equity"], 2)})
            s["last_exit"][pair] = {"day": today,
                                    "level": pos["entry"]}
            del s["positions"][pair]
            log.info("EXIT %s (%s) pnl=%.2f peak=%.1f%%",
                     pair, reason, pnl, gain * 100)
        else:
            log.info("HOLD %s close=%.6g stop=%.6g",
                     pair, close, pos["stop"])
        save_state(s)
    if len(s["positions"]) < SLOTS:
        for pair in uni:
            if len(s["positions"]) >= SLOTS:
                break
            if pair in s["positions"]:
                continue
            le = s["last_exit"].get(pair)
            try:
                raw = client.get_ohlc(pair, interval=1440)
                time.sleep(PAUSE)
            except Exception:
                continue
            raw = raw[:-1]
            close = float(raw[-1][4])
            if le and today - le["day"] < REENTRY_DAYS \
                    and close <= le["level"]:
                continue
            br = buy_ratio_24h(client, pair)
            time.sleep(PAUSE)
            ok, detail = entry_gates(raw, br)
            if not ok:
                log.info("REFUSE %s %s", pair, detail)
                continue
            alloc = s["equity"] * ALLOC
            entry = close * (1 + SLIP)
            stop = initial_stop(raw, entry)
            s["positions"][pair] = {"entry": entry,
                "volume": alloc / entry, "stop": stop,
                "high_water": close, "opened_day": today,
                "gates": detail}
            save_state(s)
            log.info("ENTER %s entry=%.6g stop=%.6g %s",
                     pair, entry, stop, detail)
    log.info("BEAT end. Equity=%.2f positions=%d",
             s["equity"], len(s["positions"]))


if __name__ == "__main__":
    beat()
