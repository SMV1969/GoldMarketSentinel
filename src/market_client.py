import requests
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        config = st.secrets.get("market_data", {})
        self.api_key = config.get("api_key")
        self.base_url = "https://www.alphavantage.co/query"

    def _fetch_api(self, params):
        """Internal helper to handle the request logic."""
        params["apikey"] = self.api_key
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Network error: {e}")
            return {}

    def get_usdinr(self):
        """Forex endpoint for USD to INR."""
        data = self._fetch_api({
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": "USD",
            "to_currency": "INR"
        })
        rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
        return {"value": round(float(rate), 2) if rate else "N/A"}

    def get_gold_price(self):
        """Stock/ETF endpoint for GLD."""
        data = self._fetch_api({"function": "GLOBAL_QUOTE", "symbol": "GLD"})
        price = data.get("Global Quote", {}).get("05. price")
        return {"value": round(float(price), 2) if price else "N/A"}