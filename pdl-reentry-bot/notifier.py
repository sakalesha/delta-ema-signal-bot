import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# Force load .env from current directory with BOM handling
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), encoding='utf-8-sig')

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def _send_async(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Bot token or Chat ID not found in environment variables.")
        return
        
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")
        
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

def send_alert(msg):
    try:
        asyncio.run(_send_async(msg))
    except Exception as e:
        print(f"Event loop error in notifier: {e}")
