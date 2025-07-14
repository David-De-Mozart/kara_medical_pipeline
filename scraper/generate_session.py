from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

with TelegramClient("telegram_session", api_id, api_hash) as client:
    print("Session created and authorized.")
