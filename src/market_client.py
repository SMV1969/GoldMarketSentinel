import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # We don't need API keys anymore. 
        # yfinance pulls data directly from public financial pages.
        pass

    def _fetch_price(self, symbol):
        """Fetches the last price for a given symbol."""
        try:
            ticker = yf.Ticker(symbol)
            # 'fast_info' is a very lightweight, fast way to get the latest price
            # without downloading entire historical datasets.
            price = ticker.fast_info['last_price']
            return round(float(price), 2) if price else "N/A"
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return "N/A"

    def get_usdinr(self):
        # INR=X is the reliable ticker for USD to INR exchange rate
        return {"value": self._fetch_price("INR=X")}

    def get_gold_price(self):
        # GLD is the gold ETF. It is highly liquid and always available.
        return {"value": self._fetch_price("GLD")}