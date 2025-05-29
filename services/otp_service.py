import random
import string
import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Redis connection setup
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class OTPService:
    def __init__(self, redis_client, default_expiry_seconds=60, max_attempts=3):
        self.redis = redis_client
        self.default_expiry = default_expiry_seconds  # Default OTP validity in seconds
        self.max_attempts = max_attempts  # Max allowed attempts per OTP

    def generate_otp(self, phone_number, length=6, expiry_seconds=None):
        """Generate and store a numeric OTP for a phone number. Optionally set custom expiry."""
        otp = ''.join(random.choices(string.digits, k=length))
        key = f"otp:{phone_number}"
        expiry = expiry_seconds if expiry_seconds is not None else self.default_expiry
        self.redis.setex(key, expiry, otp)
        # Reset attempt counter
        self.redis.setex(f"otp_attempts:{phone_number}", expiry, 0)
        return otp

    def validate_otp(self, phone_number, otp):
        """Validate the OTP for a phone number. Returns True if valid, else False. Enforces attempt limits."""
        key = f"otp:{phone_number}"
        attempts_key = f"otp_attempts:{phone_number}"
        stored_otp = self.redis.get(key)
        if not stored_otp:
            return False  # OTP expired or not set
        # Increment attempt counter
        attempts = self.redis.incr(attempts_key)
        if attempts > self.max_attempts:
            self.redis.delete(key)
            self.redis.delete(attempts_key)
            return False  # Too many attempts
        if stored_otp == otp:
            self.redis.delete(key)  # Invalidate OTP after use
            self.redis.delete(attempts_key)
            return True
        return False

    def resend_otp(self, phone_number, length=6, expiry_seconds=None):
        """Generate and store a new OTP, overwriting any existing one. Optionally set custom expiry."""
        return self.generate_otp(phone_number, length, expiry_seconds)

    def is_otp_valid(self, phone_number):
        """Check if a valid OTP exists for the phone number."""
        key = f"otp:{phone_number}"
        return self.redis.exists(key)
