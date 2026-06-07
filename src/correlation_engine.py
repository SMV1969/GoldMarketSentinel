from src.fred_client import FredClient
from src.market_client import MarketClient


class CorrelationEngine:

    def __init__(self):
        self.fred = FredClient()
        self.market = MarketClient()

    def compute(self):

        yield_val = self.fred.get_real_yield()["value"]
        usd = self.market.get_usdinr()["value"]
        gold = self.market.get_gold_price()["value"]

        score = 0

        if yield_val < 1.8:
            score += 2
        elif yield_val > 2.0:
            score -= 2

        if usd > 83.5:
            score += 1
        elif usd < 82.5:
            score -= 1

        if gold > 2300:
            score += 1
        elif gold < 2250:
            score -= 1

        return {
            "yield": yield_val,
            "usdinr": usd,
            "gold": gold,
            "score": score
        }