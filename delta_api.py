import requests
import pandas as pd
import time

BASE_URL = "https://cdn.india.deltaex.org/v2/history/candles"

def fetch_candles(symbol, resolution, limit=100):
    end = int(time.time())

    if resolution.endswith("m"):
        sec = int(resolution[:-1]) * 60
    elif resolution.endswith("h"):
        sec = int(resolution[:-1]) * 3600
    else:
        raise ValueError("Unsupported resolution")

    start = end - (sec * limit)

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "start": start,
        "end": end
    }

    r = requests.get(BASE_URL, params=params)
    data = r.json()["result"]

    df = pd.DataFrame(
        data,
        columns=["time", "open", "high", "low", "close", "volume"]
    )
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df.sort_values("time")
