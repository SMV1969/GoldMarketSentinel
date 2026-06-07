from src.fred_client import FredClient

client = FredClient()

data = client.get_real_yield()

print(data)