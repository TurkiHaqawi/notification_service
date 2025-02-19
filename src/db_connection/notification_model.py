from sqlalchemy import Column, Integer, String, JSON, Text, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from src.db_connection.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(String, primary_key=True)
    notification_type = Column(Enum("SMS", "EMAIL", "PUSH", name="notification_type_enum"), nullable=False)
    notification_template = Column(String, nullable=False)
    priority = Column(Enum("high", "medium", "low", name="priority_enum"), nullable=True)
    status = Column(Enum("pending", "sent", "failed", name="status_enum"), nullable=False, default="pending")
    data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()", onupdate="now()")

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, unique=True, nullable=False)
    notification_type = Column(String, nullable=False)
    language = Column(String, nullable=False, default="en")
    subject = Column(Text)
    body = Column(Text, nullable=False)
    placeholders = Column(JSON, nullable=False)
