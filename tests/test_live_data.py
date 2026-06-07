from src.market_client import MarketClient
from src.fred_client import FredClient

print("Testing Live Market Data...")

m = MarketClient()
f = FredClient()

print("USDINR:", m.get_usdinr())
print("Gold:", m.get_gold_price())
print("Yield:", f.get_real_yield())

print("TEST COMPLETE")