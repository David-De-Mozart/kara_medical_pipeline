import os
import psycopg2
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()

# Connect to Postgres
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

# Create schema and table
cur.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
cur.execute("""
CREATE TABLE IF NOT EXISTS analytics.fct_image_detections (
    detection_id SERIAL PRIMARY KEY,
    message_id INTEGER,
    detected_object_class TEXT,
    confidence_score FLOAT,
    image_path TEXT
);
""")
conn.commit()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Loop over images
IMAGE_DIR = "images"
for filename in os.listdir(IMAGE_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(IMAGE_DIR, filename)

        # ✅ Skip empty or invalid files
        if not os.path.isfile(img_path) or os.path.getsize(img_path) == 0:
            print(f"⚠️ Skipping empty or missing file: {img_path}")
            continue

        # Extract message_id
        try:
            message_id = int(filename.split("_")[-1].split(".")[0])
        except:
            print(f"⚠️ Could not extract message_id from filename: {filename}")
            continue

        # Run YOLO detection with try/except
        try:
            results = model(img_path)
        except Exception as e:
            print(f"❌ Failed to process image {img_path}: {e}")
            continue

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls)
                cls_name = model.names[cls_id]
                confidence = float(box.conf)

                cur.execute("""
                    INSERT INTO analytics.fct_image_detections (message_id, detected_object_class, confidence_score, image_path)
                    VALUES (%s, %s, %s, %s)
                """, (message_id, cls_name, confidence, img_path))

conn.commit()
cur.close()
conn.close()

print("✅ YOLO detection results saved to PostgreSQL.")
