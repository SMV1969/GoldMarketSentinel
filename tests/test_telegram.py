import requests

BOT_TOKEN = "8344762805:AAGR19nBFtvcy0hhCzPa4SbzZrCbzXlsF9E"
CHAT_ID = "1716061737"

message = """
✅ Market Sentinel Test

Telegram notifications are operational.
"""

url = f"https://api.telegram.org/bot8344762805:AAGR19nBFtvcy0hhCzPa4SbzZrCbzXlsF9E/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, json=payload)

print(response.json())