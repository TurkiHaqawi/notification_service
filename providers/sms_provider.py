import logging
from twilio.rest import Client as TwilioClient
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Twilio client
twilio_client = TwilioClient(account_sid=os.getenv("account_sid"), auth_token=os.getenv("auth_token"))

# Initialize AWS SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

def send_sms_twilio(to_number, message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=os.getenv("twilio_number"),
            to=to_number
        )
        return True, None
    except Exception as e:
        logging.error(f"Twilio failed: {e}")
        return False, str(e)

def send_sms_sns(to_number, message):
    try:
        sns_client.publish(
            PhoneNumber=to_number,
            Message=message
        )
        return True, None
    except ClientError as e:
        logging.error(f"AWS SNS failed: {e}")
        return False, str(e)
