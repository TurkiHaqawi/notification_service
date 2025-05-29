from fastapi import FastAPI, Query, HTTPException, Body
import threading
from services.notification_consumer import consume_notification
from services.template_service import handle_getting_all_templates, handle_getting_specific_template, handle_update_template
from models.template_models import TemplateResponse, UpdateTemplate
from models.otp_models import OTPRequest, OTPValidateRequest
from db_connection.database import get_db
from services.otp_service import OTPService, redis_client

app = FastAPI()

otp_service = OTPService(redis_client)

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

@app.post("/otp/generate")
def generate_otp_api(request: OTPRequest):
    otp = otp_service.generate_otp(request.phone_number, request.length, request.expiry_seconds)
    # In production, send the OTP via notification provider here
    return {"message": "OTP generated and sent", "phone_number": request.phone_number, "OTP": otp}

@app.post("/otp/validate")
def validate_otp_api(request: OTPValidateRequest):
    if otp_service.validate_otp(request.phone_number, request.otp):
        return {"message": "OTP is valid"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP, or too many attempts")

@app.post("/otp/resend")
def resend_otp_api(request: OTPRequest):
    otp = otp_service.resend_otp(request.phone_number, request.length, request.expiry_seconds)
    # In production, send the OTP via notification provider here
    return {"message": "OTP resent and sent", "phone_number": request.phone_number}

@app.get("/otp/exists/{phone_number}")
def otp_exists_api(phone_number: str):
    exists = otp_service.is_otp_valid(phone_number)
    return {"phone_number": phone_number, "otp_exists": bool(exists)}

def start_kafka_consumer():
    thread = threading.Thread(target=consume_notification, daemon=True)
    thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

start_kafka_consumer()