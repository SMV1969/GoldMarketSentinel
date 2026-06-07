import requests
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Everything comes from the configuration file
        config = st.secrets.get("market_data", {})
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")

    def _fetch_data(self, function, symbol):
        """Standardized, robust API fetcher."""
        if not self.api_key or not self.base_url:
            logger.error("Configuration missing in secrets.toml!")
            return None
            
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status() # Catches 404/500 errors immediately
            data = response.json()
            
            # Parsing Logic
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            
            logger.warning(f"Unexpected response structure for {symbol}: {data}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while fetching {symbol}: {e}")
            return None

    def get_usdinr(self):
        # We use a standard wrapper. 
        # Note: If Alpha Vantage structure changes, you only update this method.
        val = self._fetch_data("GLOBAL_QUOTE", "INR=X")
        return {"value": val if val else "N/A"}

    def get_gold_price(self):
        val = self._fetch_data("GLOBAL_QUOTE", "GLD")
        return {"value": val if val else "N/A"}