from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8325159032:AAEJsQK41xUGSZTzlJvSKw6MBZrAKfypQxs"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# 🔑 Hugging Face API key kamu (nanti disimpan di Railway → Variables)
HF_API_KEY = os.environ.get("HF_API_KEY")

@app.route('/')
def home():
    return "Bot aktif dengan AI ringan!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # 🔥 Panggil AI dari Hugging Face
        reply = get_ai_reply(text)

        requests.post(TELEGRAM_URL, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

def get_ai_reply(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": prompt}

    # 🔹 Model ringan dari Hugging Face (bisa kamu ganti nanti)
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/gemma-2b-it",
        headers=headers, json=data
    )

    try:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif "error" in result:
            return f"[Error model]: {result['error']}"
        else:
            return "Hmm, aku belum tahu harus jawab apa 🤔"
    except Exception as e:
        return f"[Error]: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
