import requests
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Keeps exact compatibility with your app.py
        secrets = st.secrets.get("market_data", {})
        self.api_key = secrets.get("finnhub_key")
        self.base_url = "https://finnhub.io/api/v1/quote"

    def _fetch_price(self, symbol):
        if not self.api_key:
            logger.error("API Key missing in secrets.toml")
            return "N/A"
            
        try:
            params = {"symbol": symbol, "token": self.api_key}
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # This logs the actual status code to help you debug
            if response.status_code != 200:
                logger.error(f"API returned status {response.status_code} for {symbol}")
                return "N/A"
                
            data = response.json()
            
            # Finnhub returns 'c' (current price)
            price = data.get('c')
            
            if price and price > 0:
                return round(float(price), 2)
            else:
                logger.warning(f"Symbol {symbol} returned empty data: {data}")
                return "N/A"
                
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return "N/A"

    def get_usdinr(self):
        # Existing method name preserved
        # Note: If FX:USDINR fails, try 'USDINR'
        return {"value": self._fetch_price("FX:USDINR")}

    def get_gold_price(self):
        # Existing method name preserved
        return {"value": self._fetch_price("GLD")}