# Changed
import requests
import streamlit as st

class MarketClient:
    def __init__(self):
        # Load configs from secrets
        endpoints = st.secrets.get("endpoints", {})
        self.usdinr_url = endpoints.get("usdinr_url")
        self.gold_url = endpoints.get("gold_api_url")
        
        secrets = st.secrets.get("market_data", {})
        self.finnhub_key = secrets.get("finnhub_key")

    def get_usdinr(self):
        try:
            # Flexible, not hard-coded
            response = requests.get(self.usdinr_url, timeout=10)
            data = response.json()
            return {"value": round(float(data['rates']['INR']), 2)}
        except Exception:
            return {"value": "N/A"}

    def get_gold_price(self):
        try:
            params = {"symbol": "GLD", "token": self.finnhub_key}
            response = requests.get(self.gold_url, params=params, timeout=10)
            data = response.json()
            return {"value": round(float(data.get('c')), 2)}
        except Exception:
            return {"value": "N/A"}