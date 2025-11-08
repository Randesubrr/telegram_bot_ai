from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8325159032:AAEJsQK41xUGSZTzlJvSKw6MBZrAKfypQxs"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

HF_API_KEY = os.environ.get("HF_API_KEY")
HF_MODEL = "gpt2"  # kamu bisa ganti model ini nanti

@app.route('/')
def home():
    return "Bot AI aktif!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        # 🔹 Panggil Hugging Face API
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {
            "inputs": f"Kamu adalah asisten ramah. Jawab pesan berikut dengan sopan:\n\n{user_text}"
        }

        response = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}",
            headers=headers,
            json=payload,
        )
        print("DEBUG HF:", response.status_code, response.text)

        if response.ok:
            result = response.json()
            try:
                ai_reply = result[0]["generated_text"]
            except Exception:
                ai_reply = "Maaf, aku belum bisa memproses jawaban."
        else:
            ai_reply = "Maaf, server AI sedang sibuk."

        # 🔹 Kirim balasan ke Telegram
        requests.post(TELEGRAM_URL, json={"chat_id": chat_id, "text": ai_reply})

    return {"ok": True}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
