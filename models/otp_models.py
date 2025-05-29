from pydantic import BaseModel

class OTPRequest(BaseModel):
    phone_number: str
    length: int = 6
    expiry_seconds: int | None = None

class OTPValidateRequest(BaseModel):
    phone_number: str
    otp: str
