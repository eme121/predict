import requests
import config

def send_prediction_to_telegram(message, bot_token, chat_id):
    """Send daily predictions to Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
        print("✅ Telegram alert sent")
    except:
        print("Telegram setup incomplete - add your bot token")