from src.fred_client import FredClient


class RuleEngine:
    """
    Single responsibility:
    Evaluate market conditions and return alerts.
    """

    def __init__(self):
        self.fred = FredClient()

    def evaluate(self) -> list[dict]:
        """
        Returns list of alerts (empty if no signal)
        """

        data = self.fred.get_real_yield()
        value = data["value"]

        alerts = []

        if value < 1.80:
            alerts.append({
                "subject": "Bullish Gold Signal",
                "message": f"Real Yield = {value:.2f}%\nBullish environment for gold."
            })

        elif value > 2.00:
            alerts.append({
                "subject": "Gold Headwind Warning",
                "message": f"Real Yield = {value:.2f}%\nBearish environment for gold."
            })

        return alerts