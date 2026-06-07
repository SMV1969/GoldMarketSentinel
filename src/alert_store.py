# Inside src/alert_store.py
import os
import json

# Force the file path to stay absolute, regardless of where the app is executed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALERTS_FILE = os.path.join(BASE_DIR, "alerts.json")

def alert_already_sent(alert_key):
    if not os.path.exists(ALERTS_FILE):
        return False
    try:
        with open(ALERTS_FILE, "r") as f:
            data = json.load(f)
            return alert_key in data
    except Exception:
        return False

def save_alert(alert_key):
    data = []
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = []
            
    if alert_key not in data:
        data.append(alert_key)
        
    try:
        with open(ALERTS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        # Prevent the cloud server from crashing if the drive is completely read-only
        pass