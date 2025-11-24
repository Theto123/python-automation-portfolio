import requests, time

TOKEN = "YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    return requests.get(URL + "getUpdates", params={"offset": offset}).json()

def send(chat, text):
    requests.get(URL + "sendMessage", params={"chat_id": chat, "text": text})

def run():
    last = None
    while True:
        updates = get_updates(last)
        for u in updates.get("result", []):
            last = u["update_id"] + 1
            chat = u["message"]["chat"]["id"]
            send(chat, u["message"]["text"])

if __name__ == "__main__":
    run()