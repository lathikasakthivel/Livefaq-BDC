# data_ingest_youtube.py
import time
from googleapiclient.discovery import build
from kafka import KafkaProducer
import json
from preprocess import clean_text

API_KEY = "YOUR_YOUTUBE_API_KEY"
LIVE_CHAT_ID = "YOUR_LIVE_CHAT_ID"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

def fetch_live_comments():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    response = youtube.liveChatMessages().list(
        liveChatId=LIVE_CHAT_ID,
        part="snippet,authorDetails"
    ).execute()

    messages = response.get("items", [])

    for msg in messages:
        text = msg["snippet"]["displayMessage"]
        cleaned = clean_text(text)

        data = {
            "username": msg["authorDetails"]["displayName"],
            "message": cleaned,
            "timestamp": msg["snippet"]["publishedAt"]
        }

        producer.send("livefaq_raw", value=data)
        print("Sent →", data)

if __name__ == "__main__":
    print("Starting YouTube → Kafka ingestion...")
    while True:
        try:
            fetch_live_comments()
            time.sleep(5)
        except Exception as e:
            print("Error:", e)
            time.sleep(10)
