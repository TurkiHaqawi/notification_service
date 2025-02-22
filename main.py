from fastapi import FastAPI
import threading
from services.notification_consumer import consume_notification

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Notification Service is running"}

def start_kafka_consumer():
    thread = threading.Thread(target=consume_notification, daemon=True)
    thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

start_kafka_consumer()