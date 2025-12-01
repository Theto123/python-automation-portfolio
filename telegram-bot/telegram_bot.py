import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOKEN = "YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{TOKEN}/"
SLEEP_TIME = 1

def get_updates(offset=None, timeout=30):
    """Fetch updates from Telegram API with optional offset and timeout"""
    try:
        resp = requests.get(URL + "getUpdates", params={"offset": offset, "timeout": timeout}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logging.error(f"Failed to get updates: {e}")
        return {"result": []}

def send_message(chat_id, text, reply_markup=None):
    """Send message with optional inline keyboard"""
    try:
        payload = {"chat_id": chat_id, "text": text}
        if reply_markup:
            payload["reply_markup"] = reply_markup
        requests.get(URL + "sendMessage", params=payload, timeout=10)
    except requests.RequestException as e:
        logging.error(f"Failed to send message to {chat_id}: {e}")

def handle_command(chat_id, text):
    """Process commands and send appropriate responses"""
    if text.startswith("/start"):
        send_message(chat_id, "Welcome! I am your advanced bot 🤖")
    elif text.startswith("/help"):
        send_message(chat_id, "Available commands:\n/start\n/help\n/echo <message>")
    elif text.startswith("/echo"):
        msg = text[6:] if len(text) > 5 else "You didn't provide a message."
        send_message(chat_id, f"Echo: {msg}")
    else:
        send_message(chat_id, f"You said: {text}")

def run_bot():
    """Main bot loop"""
    last_update_id = None
    logging.info("Bot started...")
    while True:
        updates = get_updates(offset=last_update_id)
        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            if "message" not in update:
                continue
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            logging.info(f"Received message from {chat_id}: {text}")
            handle_command(chat_id, text)
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    run_bot()
