from src.rule_engine import RuleEngine
from src.notification_manager import notify_all


def main():

    print("Market Sentinel Starting...")

    engine = RuleEngine()

    alerts = engine.evaluate()

    if not alerts:
        print("No signals. System idle.")
        return

    for alert in alerts:

        print("Trigger:", alert["subject"])

        notify_all(
            subject=alert["subject"],
            message=alert["message"]
        )

    print("Run complete.")


if __name__ == "__main__":
    main()