import yfinance as yf
import time
import logging
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Create a session that mimics a real web browser
        self.session = Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Add retry logic: If it fails, wait 5, 10, then 20 seconds before giving up
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _fetch_price(self, symbol):
        """Fetch using yfinance with session injection."""
        try:
            ticker = yf.Ticker(symbol, session=self.session)
            # Fetch data with a custom market_client session
            data = ticker.fast_info
            price = data['last_price']
            return round(float(price), 2)
        except Exception as e:
            logger.error(f"Provider limit hit for {symbol}. Moving to fallback.")
            return "N/A"

    def get_usdinr(self):
        return {"value": self._fetch_price("INR=X")}

    def get_gold_price(self):
        return {"value": self._fetch_price("GLD")}