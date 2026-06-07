import yfinance as yf

class MarketClient:
    def get_usdinr(self):
        try:
            ticker = yf.Ticker("INR=X")
            data = ticker.history(period="1d")
            if data.empty:
                print("DEBUG: YFinance USDINR returned empty data.")
                return {"value": 0.0}
            return {"value": round(data['Close'].iloc[-1], 2)}
        except Exception as e:
            print(f"DEBUG CRITICAL: USDINR failure: {str(e)}") # This will print the actual error
            return {"value": 0.0}

    def get_gold_price(self):
        try:
            ticker = yf.Ticker("GC=F")
            data = ticker.history(period="1d")
            if data.empty:
                print("DEBUG: YFinance Gold returned empty data.")
                return {"value": 0.0}
            return {"value": round(data['Close'].iloc[-1], 2)}
        except Exception as e:
            print(f"DEBUG CRITICAL: Gold failure: {str(e)}") # This will print the actual error
            return {"value": 0.0}