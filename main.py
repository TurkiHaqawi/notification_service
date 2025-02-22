from fastapi import FastAPI, Query
import threading
from services.notification_consumer import consume_notification
from services.template_service import handle_getting_all_templates, handle_getting_specific_template, handle_update_template
from db_connection.response_serialization import TemplateResponse, UpdateTemplate

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Notification Service is running"}

@app.get("/templates", response_model=list[TemplateResponse])
def get_all_templates(notification_type: str = Query(None, regex="^(SMS|EMAIL|PUSH)$")):
    """ Retrieve all templates, optionally filtering by notification_type. """
    return handle_getting_all_templates(notification_type)

@app.get("/templates/{template_name}", response_model=TemplateResponse)
def get_template(template_name: str):
    """ Retrieve a single notification template by template_name. """
    return handle_getting_specific_template(template_name)

@app.put("/templates/{template_name}")
def update_template(template_name: str, template_update: UpdateTemplate):
    return handle_update_template(template_name, template_update)

def start_kafka_consumer():
    thread = threading.Thread(target=consume_notification, daemon=True)
    thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

start_kafka_consumer()