from flask import Flask, request
import requests

app = Flask(name)

TOKEN = "8478311707:AAFF4Zpw1f1n2ChYjjsqu897I_S-VmW_l_U"
CHAT_ID = "8036962371"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

@app.route('/')
def home():
    return "Bot running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = f"Signal: {data}"
    send_telegram(message)
    return "ok"

app.run(host='0.0.0.0', port=10000)
