import asyncio
from telegram import Bot
import os

BOT_TOKEN = "7959899285:AAEYQH_kyc_1i7j7LA85PaFcFKeRP7PbMcs"
CHAT_ID = "6640875299"

async def _send_async(msg):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

def send_alert(msg):
    try:
        asyncio.run(_send_async(msg))
    except Exception as e:
        print(f"Failed to send alert: {e}")
