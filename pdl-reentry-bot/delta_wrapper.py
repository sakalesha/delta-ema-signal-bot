import requests
import pandas as pd
import time
import config

# Use the specific endpoint that was working for the user
BASE_URL = "https://cdn.india.deltaex.org/v2/history/candles"

def fetch_candles(symbol, resolution, limit=100):
    """
    Fetches candles from Delta Exchange.
    resolution: '1m', '15m', '1h', '1d' etc.
    """
    end = int(time.time())

    # Calculate start time based on resolution and limit
    if resolution.endswith("m"):
        sec = int(resolution[:-1]) * 60
    elif resolution.endswith("h"):
        sec = int(resolution[:-1]) * 3600
    elif resolution.endswith("d"):
        sec = int(resolution[:-1]) * 86400
    else:
        # Default fallback or error
        raise ValueError(f"Unsupported resolution: {resolution}")

    start = end - (sec * limit)

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "start": start,
        "end": end
    }

    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json().get("result", [])
        
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(
            data,
            columns=["time", "open", "high", "low", "close", "volume"]
        )
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df.sort_values("time").reset_index(drop=True)
    except Exception as e:
        print(f"Error fetching candles: {e}")
        return pd.DataFrame()
