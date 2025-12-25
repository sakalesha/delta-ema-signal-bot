import requests
import pandas as pd
from datetime import datetime
import time

def fetch_candles(symbol, resolution):
    base_url = "https://cdn.india.deltaex.org/v2/history/candles"
    end_time = int(time.time())
    # Resolution usually int minutes for calculation, but string for API?
    # Actually Delta API expects "15m" etc.
    res_min = 15
    start_time = end_time - (res_min * 60 * 5) # Last 5 candles
    
    params = {
        "symbol": symbol,
        "resolution": resolution, # "15m"
        "start": start_time,
        "end": end_time
    }
    
    response = requests.get(base_url, params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json().get("result")
        if not data:
             print("No data in result key!")
             print(response.json())
             return None
        df = pd.DataFrame(data)
        # Convert timestamp (seconds) to datetime
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df
    else:
        print("API Error:", response.text)
    return None

now = datetime.now()
print(f"Current System Time: {now}")

df = fetch_candles("BTCUSD", "15m")
if df is not None:
    print("\nLast 3 Candles from API:")
    print(df.tail(3)[["time", "close"]])
    
    last_candle_time = df.iloc[-1]["time"]
    print(f"\niloc[-1] Time: {last_candle_time}")
    
    # Check if iloc[-1] is the just-closed candle or forming
    # If now is 14:16, and iloc[-1] is 14:00 (Close 14:15), then iloc[-1] is the JUST CLOSED candle.
    # If iloc[-1] is 14:15 (Open), then it is the FORMING candle.
    
    diff_min = (now - last_candle_time).total_seconds() / 60
    print(f"Difference from Now (min): {diff_min:.2f}")

