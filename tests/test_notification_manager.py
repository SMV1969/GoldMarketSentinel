from src.notification_manager import notify_all

print("Starting Notification Manager Test...")

notify_all(
    subject="Market Sentinel Test",
    message="Notification Manager Working"
)

print("TEST PASSED")