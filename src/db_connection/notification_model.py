from sqlalchemy import Column, Integer, String, JSON, Text
from src.db_connection.database import Base

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, unique=True, nullable=False)
    notification_type = Column(String, nullable=False)
    language = Column(String, nullable=False, default="en")
    subject = Column(Text)
    body = Column(Text, nullable=False)
    placeholders = Column(JSON, nullable=False)
