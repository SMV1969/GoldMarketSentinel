import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketClient:
    def __init__(self):
        # Create a persistent session
        self.session = yf.shared.get_session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _get_last_price(self, symbol):
        """Helper to fetch the last valid closing price."""
        try:
            # We fetch 1 month of data to ensure we have a valid last close
            ticker = yf.Ticker(symbol, session=self.session)
            data = ticker.history(period="1mo")
            
            if data.empty or 'Close' not in data:
                logger.warning(f"No data returned for {symbol}")
                return None
            
            # Get the last non-empty closing price
            last_price = data['Close'].dropna().iloc[-1]
            return round(float(last_price), 2)
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return None

    def get_usdinr(self):
        val = self._get_last_price("INR=X")
        return {"value": val if val is not None else "N/A"}

    def get_gold_price(self):
        val = self._get_last_price("GLD")
        return {"value": val if val is not None else "N/A"}