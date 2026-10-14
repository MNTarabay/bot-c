import pandas as pd

from botc.config import P

X = P["exit"]


def swing_lows(raw_daily, lookback=X["swing_lookback"]):
    df = pd.DataFrame(raw_daily,
        columns=["t","o","h","l","c","vw","v","n"])
    l = df["l"].astype(float).values
    lows = []
    for i in range(lookback, len(l) - lookback):
        if l[i] <= min(l[i - lookback:i + lookback + 1]):
            lows.append((i, float(l[i])))
    return lows


def initial_stop(raw_daily, entry_price, max_risk=X["max_risk"]):
    lows = swing_lows(raw_daily)
    candidates = [p for _, p in lows if p < entry_price]
    if candidates:
        stop = candidates[-1] * X["stop_buffer"]
    else:
        stop = entry_price * (1 - max_risk)
    floor = entry_price * (1 - max_risk)
    return max(stop, floor)


def trail_stop(raw_daily, entry_price, current_stop, gain):
    if gain < X["trail_arm_gain"]:
        return current_stop
    lows = swing_lows(raw_daily)
    if not lows:
        return current_stop
    newest = lows[-1][1] * X["stop_buffer"]
    return max(current_stop, newest)
