import firebase_admin
from firebase_admin import messaging, credentials
from dotenv import load_dotenv

load_dotenv()

# Load Firebase credentials
firebase_credentials_path = "/notification_service/firebase_config.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)

class FCMNotification:
    def __init__(self):
        pass

    def send_push_notification(self, device_token, title, message):
        try:
            notification = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message
                ),
                token=device_token
            )
            response = messaging.send(notification)
            return {"status": "sent", "message_id": response}
        except Exception as e:
            print(f"FCM Push Error: {e}")
            return {"status": "failed", "error": str(e)}
