import requests
from src.data_providers.cache import get_cached, set_cache

URL = "https://query1.finance.yahoo.com/v8/finance/chart/INR=X"


def get_usdinr():

    cached = get_cached("usdinr")
    if cached:
        return cached

    try:
        r = requests.get(URL, timeout=5)
        data = r.json()

        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

        result = {
            "symbol": "USDINR",
            "value": float(price)
        }

        set_cache("usdinr", result)
        return result

    except Exception:
        # fallback safety
        return {
            "symbol": "USDINR",
            "value": 83.0
        }
