import yfinance as yf

class MarketClient:
    """
    Direct live data client using Yahoo Finance.
    """

    def get_usdinr(self):
        try:
            ticker = yf.Ticker("INR=X")
            data = ticker.history(period="1d")
            return {"value": round(data['Close'].iloc[-1], 2) if not data.empty else 0.0}
        except Exception as e:
            print(f"Error fetching USDINR: {e}")
            return {"value": 0.0}

    def get_gold_price(self):
        try:
            ticker = yf.Ticker("GC=F")
            data = ticker.history(period="1d")
            return {"value": round(data['Close'].iloc[-1], 2) if not data.empty else 0.0}
        except Exception as e:
            print(f"Error fetching Gold: {e}")
            return {"value": 0.0}