import yfinance as yf

class MarketClient:
    def get_usdinr(self):
        try:
            # Forex (INR=X) usually has weekend quotes, so this stays as is
            ticker = yf.Ticker("INR=X")
            data = ticker.history(period="1d")
            return {"value": round(data['Close'].iloc[-1], 2) if not data.empty else 0.0}
        except Exception:
            return {"value": 0.0}

    def get_gold_price(self):
        try:
            # Change period to 5d to ensure we catch the last Friday close if today is Sunday
            ticker = yf.Ticker("GLD") 
            data = ticker.history(period="5d")
            # This line grabs the last valid row, even if today is empty
            last_valid_price = data['Close'].dropna().iloc[-1]
            return {"value": round(last_valid_price, 2)}
        except Exception as e:
            print(f"DEBUG: Gold fetch error: {e}")
            return {"value": 0.0}