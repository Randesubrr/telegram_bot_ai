from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8325159032:AAEJsQK41xUGSZTzlJvSKw6MBZrAKfypQxs"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/')
def home():
    return "Bot aktif!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        reply = f"Halo! Kamu mengirim: {text}"
        requests.post(URL, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)