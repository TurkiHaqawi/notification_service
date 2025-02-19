from confluent_kafka import Consumer
from sqlalchemy.orm import Session
from src.db_connection.database import get_db
from src.db_connection.notification_model import Notification
from sqlalchemy.orm import Session
import json
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "bootstrap.servers": os.getenv("bootstrap.servers"),
    "security.protocol": os.getenv("security.protocol"),
    "sasl.mechanisms": os.getenv("sasl.mechanisms"),
    "sasl.username": os.getenv("sasl.username"),
    "sasl.password": os.getenv("sasl.password"),
    "session.timeout.ms": os.getenv("session.timeout.ms"),
    "group.id": "notification_service",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
}

consumer = Consumer(config)
consumer.subscribe(["notifications_topic"])

def process_notification():
    db: Session = next(get_db())


    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        notification_data = json.loads(msg.value().decode("utf-8"))
        print(notification_data)
        