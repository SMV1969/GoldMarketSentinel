import os
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()


class FredClient:
    """
    FRED API Client
    """

    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self):
        self.api_key = os.getenv("FRED_API_KEY")

        if not self.api_key:
            raise ValueError(
                "FRED_API_KEY not found in environment variables."
            )

    def get_latest_observation(self, series_id: str) -> dict:
        """
        Fetch latest observation for a FRED series.
        """

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1,
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        observations = data.get("observations", [])

        if not observations:
            raise ValueError(
                f"No observations returned for {series_id}"
            )

        obs = observations[0]

        return {
            "series_id": series_id,
            "date": obs["date"],
            "value": float(obs["value"])
        }

    def get_real_yield(self) -> dict:
        """
        DFII10 = 10-Year Treasury Inflation Indexed Security
        """

        return self.get_latest_observation("DFII10")