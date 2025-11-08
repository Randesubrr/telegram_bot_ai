from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8325159032:AAEJsQK41xUGSZTzlJvSKw6MBZrAKfypQxs")
HF_API_KEY = os.getenv("HF_API_KEY")

@app.route('/')
def home():
    return "Bot aktif dengan AI (Zephyr)!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # kirim ke model HF
        HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"
        HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": text}

        try:
            response = requests.post(HF_URL, headers=headers, json=payload, timeout=20)
            print("DEBUG HF:", response.status_code, response.text)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                    reply = data[0]["generated_text"]
                else:
                    reply = "AI tidak mengembalikan teks 😅"
            else:
                reply = "Maaf, AI sedang sibuk."
        except Exception as e:
            print("ERROR HF:", e)
            reply = "Terjadi kesalahan saat menghubungi AI."

        # kirim balasan ke Telegram
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": reply})

    return {"ok": True}
    print("DEBUG TOKEN:", HF_API_KEY[:6] if HF_API_KEY else "NOT FOUND")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
