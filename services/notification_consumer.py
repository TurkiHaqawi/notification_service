from confluent_kafka import Consumer
from sqlalchemy.orm import Session
from db_connection.database import get_db
from db_connection.notification_model import Notification
from services.notification_service import NotificationService
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

def consume_notification():
    db: Session = next(get_db())


    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            continue

        notification_data = json.loads(msg.value().decode("utf-8"))
        notification_id = notification_data["notificationId"]

        # Check if notification already exists (Idempotency Check)
        existing_notification = db.query(Notification).filter_by(notification_id=notification_id).first()
        if existing_notification:
            consumer.commit()
            continue

        processed_notification = NotificationService()
        processed_notification.send_notification(notification_data)
        
        consumer.commit()