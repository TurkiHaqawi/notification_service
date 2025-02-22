from sqlalchemy.orm import Session
from db_connection.database import get_db
from db_connection.notification_model import NotificationTemplate
from services.provider_manager import send_sms, send_email
import logging

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_notification_template(self, template_name):
        """ Fetches the notification template from the database. """
        return self.db.query(NotificationTemplate).filter_by(template_name=template_name).first()
    
    def format_message(self, template_body, data):
        """ Replaces placeholders in the template with actual values. """
        for key, value in data.items():
            template_body = template_body.replace(f"{{{{ {key} }}}}", value)
        return template_body
    
    def send_notification(self, notification):
        """ Fetches template, formats message, and sends notification. """
        # Fetch the template
        template = self.get_notification_template(notification.notification_template)
        if not template:
            print(f"Template {notification.notification_template} not found.")
            logging.error(notification, "Template not found")
            return False
        
        # Format the message
        message = self.format_message(template.body, notification.data)

        if notification.notification_type == "SMS":
            send_sms(notification.data.phone_number, message)
        if notification.notification_type == "EMAIL":
            send_email(notification.data.email, template.subject, message)
        if notification.notification_type == "PUSH":
            pass