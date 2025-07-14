import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

# Ensure schema and table exist
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id INTEGER,
    channel_name TEXT,
    message_text TEXT,
    message_date TIMESTAMP,
    has_photo BOOLEAN,
    image_path TEXT
);
""")
conn.commit()

# Load each file
RAW_PATH = "data/raw/telegram_messages"
for filename in os.listdir(RAW_PATH):
    if filename.endswith(".json"):
        channel_name = filename.split("_")[-1].replace(".json", "")
        with open(os.path.join(RAW_PATH, filename), "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages
                    (id, channel_name, message_text, message_date, has_photo, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    msg["id"],
                    channel_name,
                    msg.get("text"),
                    msg["date"],
                    msg.get("has_photo", False),
                    msg.get("image_path")
                ))
conn.commit()
cur.close()
conn.close()
print("✅ Loaded raw data into PostgreSQL.")
