import requests
from src.data_providers.cache import get_cached, set_cache

URL = "https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X"


def get_gold_price():

    cached = get_cached("gold")
    if cached:
        return cached

    try:
        r = requests.get(URL, timeout=5)
        data = r.json()

        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

        result = {
            "symbol": "XAUUSD",
            "value": float(price)
        }

        set_cache("gold", result)
        return result

    except Exception:
        return {
            "symbol": "XAUUSD",
            "value": 2350.0
        }