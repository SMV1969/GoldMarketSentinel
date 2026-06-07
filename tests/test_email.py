import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. Load variables
load_dotenv()

# 2. Assign variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

print(f"DEBUG: Loaded Email: '{EMAIL_USER}'")
print(f"DEBUG: Loaded Password length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0}")
print(f"Attempting to send email to: {EMAIL_TO}")

# 3. Create the message object
msg = EmailMessage()
msg["Subject"] = "Market Sentinel Test - 2026-06-04"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg.set_content("Email notifications are operational.")

# 4. Attempt to send
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Login successful! Email sent successfully.")
except Exception as e:
    print(f"Login failed: {e}")