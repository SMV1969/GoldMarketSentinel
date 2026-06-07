import requests
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Retrieve the key from Streamlit Secrets
        config = st.secrets.get("market_data", {})
        self.api_key = config.get("finnhub_key")
        self.base_url = "https://finnhub.io/api/v1/quote"

    def _fetch_price(self, symbol):
        """Official API fetcher."""
        try:
            params = {"symbol": symbol, "token": self.api_key}
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            # 'c' stands for current price in Finnhub API
            if 'c' in data:
                return float(data['c'])
            return "N/A"
        except Exception as e:
            logger.error(f"Finnhub API Error for {symbol}: {e}")
            return "N/A"

    def get_usdinr(self):
        # Finnhub uses 'FX:USDINR' for currency
        return {"value": self._fetch_price("FX:USDINR")}

    def get_gold_price(self):
        # GLD is the ticker for the Gold ETF
        return {"value": self._fetch_price("GLD")}