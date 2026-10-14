import pandas as pd

from botc.config import P

E = P["entry"]


def entry_gates(raw_daily, buy_ratio):
    """Article 3: all five gates on daily bars. Returns (passed, detail)."""
    df = pd.DataFrame(raw_daily,
        columns=["t","o","h","l","c","vw","v","n"])
    for col in ["c","v"]:
        df[col] = df[col].astype(float)
    if len(df) < E["min_bars"]:
        return False, {"reason": "insufficient history"}
    c, v = df["c"], df["v"]
    n = E["breakout_bars"]
    ema20 = c.ewm(span=E["ema_span"]).mean()
    g1 = bool(c.iloc[-1] > ema20.iloc[-1]
              and ema20.iloc[-1] > ema20.iloc[-1 - E["ema_rise_lookback"]])
    g2 = bool(c.iloc[-1] >= c.iloc[-n - 1:-1].max())
    g3 = bool(v.iloc[-1] >= E["volume_mult"] * float(v.iloc[-n - 1:-1].median()))
    g4 = bool(buy_ratio > E["buy_ratio_min"])
    g5 = bool(c.iloc[-1] / ema20.iloc[-1] - 1 <= E["max_extension"])
    detail = {"uptrend": g1, "breakout": g2, "volume": g3,
              "flow": g4, "room": g5,
              "buy_ratio": round(buy_ratio, 3),
              "ext": round(float(c.iloc[-1] / ema20.iloc[-1] - 1), 3)}
    return all([g1, g2, g3, g4, g5]), detail
