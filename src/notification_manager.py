from src.telegram_notifier import send_telegram
from src.email_notifier import send_email


def notify_all(subject: str, message: str):

    send_telegram(message)

    send_email(
        subject=subject,
        body=message
    )