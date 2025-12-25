import time
from config import *
from delta_api import fetch_candles
from indicators import ema
from strategy import check_ema5_signal
from notifier import send_alert

last_signal = {}

while True:
    try:
        for symbol in SYMBOLS:
            df = fetch_candles(symbol, TIMEFRAME)

            df["ema5"] = ema(df["close"], EMA_PERIOD)

            c1 = df.iloc[-3]
            c2 = df.iloc[-2]
            
            # Extract EMA values for the respective candles
            ema_c1 = c1["ema5"]
            ema_c2 = c2["ema5"]

            print(f"{symbol} | C2: {c2['time']} C={c2['close']} EMA={round(ema_c2, 2)} | C1: {c1['time']} C={c1['close']} EMA={round(ema_c1, 2)}")

            signal = check_ema5_signal(c1, c2, ema_c1, ema_c2)

            if signal:
                key = f"{symbol}_{c2['time']}"
                if key not in last_signal:
                    message = f"""
🚨 EMA 5 SIGNAL

Symbol: {symbol}
Type: {signal}
Timeframe: {TIMEFRAME}
Close: {c2['close']}
EMA5: {round(ema_c2, 2)}
Time: {c2['time']}
"""
                    send_alert(message)
                    last_signal[key] = True

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(30)
