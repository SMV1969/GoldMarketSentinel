import json
from pathlib import Path

ALERT_FILE = Path("data/alerts.json")


def alert_already_sent(alert_key: str):

    if not ALERT_FILE.exists():
        return False

    with open(ALERT_FILE, "r") as f:
        alerts = json.load(f)

    return alert_key in alerts


def save_alert(alert_key: str):

    alerts = []

    if ALERT_FILE.exists():
        with open(ALERT_FILE, "r") as f:
            alerts = json.load(f)

    if alert_key not in alerts:
        alerts.append(alert_key)

    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f)