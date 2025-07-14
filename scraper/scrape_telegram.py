import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from telethon.tl.functions.messages import GetHistoryRequest

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("telegram_session", api_id, api_hash)

channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/Medsurepharma",
    "https://t.me/StGabrielpharmacy",
    "https://t.me/PharmacistRayid",
    "https://t.me/HakimApps_Guideline",
    "https://t.me/Thequorachannel",
    "https://t.me/lobelia4cosmetics"  # Add more here
]

RAW_PATH = "data/raw/telegram_messages"
IMAGE_PATH = "images"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(IMAGE_PATH, exist_ok=True)

async def scrape_channel(channel_url):
    await client.start()
    entity = await client.get_entity(channel_url)
    history = await client(GetHistoryRequest(
        peer=entity,
        limit=500,  # increase as needed
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    messages = []
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    channel_name = channel_url.split("/")[-1]

    for msg in history.messages:
        msg_data = {
            "id": msg.id,
            "text": msg.message,
            "date": str(msg.date),
            "has_photo": bool(msg.media),
        }

        if isinstance(msg.media, MessageMediaPhoto):
            file_path = f"{IMAGE_PATH}/{channel_name}_{msg.id}.jpg"
            await client.download_media(msg.media, file=file_path)
            msg_data["image_path"] = file_path

        messages.append(msg_data)

    # Save to JSON
    save_path = f"{RAW_PATH}/{date_str}_{channel_name}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

    print(f"Saved {len(messages)} messages from {channel_url}")

with client:
    for ch in channels:
        client.loop.run_until_complete(scrape_channel(ch))
