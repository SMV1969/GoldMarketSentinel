import requests
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Let's verify secrets existence in the logs
        secrets = st.secrets.get("market_data", {})
        self.finnhub_key = secrets.get("finnhub_key")
        logger.info(f"DEBUG: Secrets loaded. Key exists: {self.finnhub_key is not None}")

    def get_usdinr(self):
        try:
            # Frankfurter does not need a key
            url = "https://api.frankfurter.app/latest?from=USD&to=INR"
            response = requests.get(url, timeout=5)
            logger.info(f"DEBUG: Frankfurter Response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                return {"value": round(float(data['rates']['INR']), 2)}
        except Exception as e:
            logger.error(f"DEBUG: Frankfurter FAILED: {e}")
            
        return {"value": "N/A"}

    def get_gold_price(self):
        try:
            # Finnhub requires a key
            if not self.finnhub_key:
                logger.error("DEBUG: Finnhub Key missing!")
                return {"value": "N/A"}
                
            url = "https://finnhub.io/api/v1/quote"
            params = {"symbol": "GLD", "token": self.finnhub_key}
            response = requests.get(url, params=params, timeout=5)
            logger.info(f"DEBUG: Finnhub Response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                return {"value": round(float(data.get('c')), 2)}
        except Exception as e:
            logger.error(f"DEBUG: Finnhub FAILED: {e}")
            
        return {"value": "N/A"}