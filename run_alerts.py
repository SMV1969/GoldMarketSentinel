# run_alerts.py
import os
import sys

# 1. Standard path setup before local imports
root_path = os.path.abspath(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.fred_client import FredClient
from src.market_client import MarketClient
from src.correlation_engine import CorrelationEngine
from src.rule_engine import RuleEngine
from src.alert_store import alert_already_sent, save_alert

def main():
    print("🤖 Sentinel Alert Engine starting background evaluation...")
    
    # Initialize components
    rule_engine = RuleEngine()
    
    # Evaluate rules to find active market signals
    try:
        alerts = rule_engine.evaluate()
    except Exception as e:
        print(f"❌ Error during rule execution: {e}")
        return

    if not alerts:
        print("💤 No active rule engine alerts triggered right now.")
        return

    print(f"🧠 Found {len(alerts)} active signal(s). Processing logs and notifications...")

    for alert in alerts:
        alert_key = alert['subject']
        
        # Check against your robust absolute-path JSON tracker
        if alert_already_sent(alert_key):
            print(f"ℹ️ [{alert_key}] has already been processed and logged. Skipping notifications.")
        else:
            print(f"🆕 NEW SIGNAL TRIGGERED: {alert_key}")
            print(f"💬 Message: {alert['message']}")
            
            # --- YOUR NOTIFICATION TRIGGERS GO HERE ---
            # This is where your local system safely fires the channels
            # send_gmail(alert['subject'], alert['message'])
            # send_telegram(alert['message'])
            # ------------------------------------------
            
            # Save it immediately using your cloud-safe file engine so it isn't sent again
            save_alert(alert_key)
            print(f"💾 Successfully saved [{alert_key}] to system logs.")

if __name__ == "__main__":
    main()