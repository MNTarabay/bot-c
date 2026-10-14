import requests

API_URL = "https://api.kraken.com"


class KrakenClient:
    """Public market-data endpoints only. Bot C never authenticates."""

    def __init__(self):
        self.session = requests.Session()

    def get_ohlc(self, pair, interval=1440, since=None):
        params = {"pair": pair, "interval": interval}
        if since:
            params["since"] = since
        data = self._public("/0/public/OHLC", params)
        key = next(k for k in data if k != "last")
        return data[key]

    def ticker_all(self):
        return self._public("/0/public/Ticker", {})

    def asset_pairs(self):
        return self._public("/0/public/AssetPairs", {})

    def trades(self, pair, since=None):
        params = {"pair": pair}
        if since:
            params["since"] = since
        return self._public("/0/public/Trades", params)

    def _public(self, path, params):
        r = self.session.get(API_URL + path, params=params, timeout=20)
        r.raise_for_status()
        out = r.json()
        if out.get("error"):
            raise RuntimeError(f"Kraken error: {out['error']}")
        return out["result"]
