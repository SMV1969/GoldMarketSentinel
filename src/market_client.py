import yfinance as yf
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _fetch_price(self, symbol):
        try:
            ticker = yf.Ticker(symbol, session=self.session)
            price = ticker.fast_info['last_price']
            return round(float(price), 2)
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return "N/A"

    def get_usdinr(self):
        return {"value": self._fetch_price("INR=X")}

    def get_gold_price(self):
        return {"value": self._fetch_price("GLD")}