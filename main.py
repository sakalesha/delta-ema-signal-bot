import time
from datetime import datetime
import threading
import os
from flask import Flask
from config import *
from delta_api import fetch_candles
from indicators import ema
from strategy import check_liquidity_sweep_signal, check_ema_crossover
from notifier import send_alert

# Flask Web Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Delta EMA Bot is Running!"

last_signal = {}

def get_sleep_time():
    now = datetime.now()
    minutes = now.minute
    seconds = now.second
    # 15 minute interval
    next_interval = ((minutes // 15) + 1) * 15
    if next_interval == 60:
        sleep_min = 60 - minutes
    else:
        sleep_min = next_interval - minutes
    
    sleep_sec = (sleep_min * 60) - seconds + 5 # 5 seconds buffer
    return sleep_sec

def run_bot():
    print("Bot started...")
    while True:
        try:
            sleep_seconds = get_sleep_time()
            print(f"Sleeping for {sleep_seconds} seconds until next candle close...")
            time.sleep(sleep_seconds)

            for symbol in SYMBOLS:
                df = fetch_candles(symbol, TIMEFRAME)

                df["ema5"] = ema(df["close"], EMA_PERIOD)

                # Need at least a few candles for history
                if len(df) < 15:
                    continue

                c1 = df.iloc[-3]
                c2 = df.iloc[-2]
                
                # Extract EMA values for the respective candles
                ema_c1 = c1["ema5"]
                ema_c2 = c2["ema5"]

                # Get recent 10 lows and highs BEFORE C1
                # C1 is at index -3. So we want slice from -13 to -3
                recent_data = df.iloc[-13:-3]
                recent_lows = recent_data["low"].tolist()
                recent_highs = recent_data["high"].tolist()

                print(f"{symbol} | C2: {c2['time']} C={c2['close']} EMA={round(ema_c2, 2)} | C1: {c1['time']} C={c1['close']} EMA={round(ema_c1, 2)}")
                
                signal = check_liquidity_sweep_signal(c1, c2, ema_c1, ema_c2, recent_lows, recent_highs)

                if signal:
                    key = f"{symbol}_{c2['time']}"
                    if key not in last_signal:
                        message = f"""
🚨 LIQUIDITY SWEEP SIGNAL

Symbol: {symbol}
Type: {signal}
Timeframe: {TIMEFRAME}
Close: {c2['close']}
EMA5: {round(ema_c2, 2)}
Time: {c2['time']}
"""
                        send_alert(message)
                        last_signal[key] = True
                
                else:
                    # Check for SETUP (Crossover) Warning
                    setup_signal = check_ema_crossover(c1, c2, ema_c1, ema_c2)
                    if setup_signal:
                        key = f"{symbol}_{c2['time']}_SETUP"
                        if key not in last_signal:
                            if setup_signal == "BEARISH_CROSS":
                                 msg_body = "📉 MINOR SETUP ALERT (Potential BUY Prep)\n\nCondition: Price Goes Below EMA 5\nInfo: Market shows short-term bearish pressure. Traps early buyers."
                            else:
                                 msg_body = "📈 MINOR SETUP ALERT (Potential SELL Prep)\n\nCondition: Price Goes Above EMA 5\nInfo: Market shows short-term bullish pressure. Traps early sellers."

                            message = f"""
{msg_body}

Symbol: {symbol}
Timeframe: {TIMEFRAME}
Close: {c2['close']}
EMA5: {round(ema_c2, 2)}
Time: {c2['time']}
"""
                            send_alert(message)
                            last_signal[key] = True

        except Exception as e:
            print("Error:", e)
            time.sleep(30)

if __name__ == "__main__":
    # Start the bot in a background thread
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    # Start the Flask web server
    # Render assigns specific port via os.environ.get("PORT")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
