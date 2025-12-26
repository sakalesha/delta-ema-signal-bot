import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), encoding='utf-8-sig')

# Delta Exchange API
BASE_URL = "https://api.delta.exchange"
SYMBOL = "BTCUSD" 
TRADING_SYMBOL = "BTCUSD" 

# Timeframes
TIMEFRAME_15M = "15m"
TIMEFRAME_1D = "1d"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Strategy Config
RISK_REWARD = 2
