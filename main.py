
from flask import Flask
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import requests

app = Flask(name)

# Telegram details
TELEGRAM_TOKEN = "8478311707:AAFF4Zpw1f1n2ChYjjsqu897I_S-VmW_l_U"
CHAT_ID = "8036962371"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

@app.route("/")
def index():
    # Initialize MT5
    if not mt5.initialize():
        return "MT5 initialize failed"
    
    # Fetch EURUSD M15 last 100 bars
    symbol = "EURUSD"
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M15, datetime.now() - timedelta(days=1), 100)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    
    # Simple Moving Average Strategy
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA20'] = data['close'].rolling(20).mean()
    
    signal = "HOLD"
    if data['MA5'].iloc[-1] > data['MA20'].iloc[-1] and data['MA5'].iloc[-2] <= data['MA20'].iloc[-2]:
        signal = "BUY"
    elif data['MA5'].iloc[-1] < data['MA20'].iloc[-1] and data['MA5'].iloc[-2] >= data['MA20'].iloc[-2]:
        signal = "SELL"
    
    # Send Telegram alert if BUY/SELL
    if signal != "HOLD":
        send_telegram(f"EURUSD M15 Signal: {signal}")
    
    mt5.shutdown()
    
    return f"Latest Signal: {signal}"

if name == "main":
    app.run(debug=True)
