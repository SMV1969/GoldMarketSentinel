from src.data_providers.fx_client import get_usdinr
from src.data_providers.gold_price_client import get_gold_price


class MarketClient:

    def get_usdinr(self):
        return get_usdinr()

    def get_gold_price(self):
        return get_gold_price()