import yfinance as yf

class MarketClient:
    def get_usdinr(self):
        try:
            # Forex data often requires a specific lookback
            ticker = yf.Ticker("INR=X")
            data = ticker.history(period="2d") # Fetch 2 days to be safe
            
            if data.empty or 'Close' not in data:
                print("DEBUG: USDINR data is empty.")
                return {"value": "N/A"}
            
            latest_val = data['Close'].iloc[-1]
            return {"value": round(float(latest_val), 2)}
        except Exception as e:
            print(f"DEBUG: USDINR Error: {e}")
            return {"value": "N/A"}

    def get_gold_price(self):
        try:
            ticker = yf.Ticker("GLD")
            data = ticker.history(period="5d")
            
            if data.empty or 'Close' not in data:
                print("DEBUG: Gold data is empty.")
                return {"value": "N/A"}
                
            # Safely get the last valid price
            valid_data = data['Close'].dropna()
            if valid_data.empty:
                return {"value": "N/A"}
                
            latest_val = valid_data.iloc[-1]
            return {"value": round(float(latest_val), 2)}
        except Exception as e:
            print(f"DEBUG: Gold Error: {e}")
            return {"value": "N/A"}