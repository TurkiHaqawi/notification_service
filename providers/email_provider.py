import logging
import requests
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize Mailgun client
MAILGUN_API_KEY = os.getenv("api_key")
MAILGUN_DOMAIN = os.getenv("domain")
MAILGUN_API_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

# Initialize AWS SES client
ses_client = boto3.client('ses', region_name='us-east-1')

def send_email_mailgun(to_email, subject, message):
    try:
        response = requests.post(
            MAILGUN_API_URL,
            auth=("api", MAILGUN_API_KEY),
            data={"from": "your-email@domain.com",
                  "to": to_email,
                  "subject": subject,
                  "text": message}
        )
        if response.status_code == 200:
            return True, None
        else:
            return False, response.text
    except Exception as e:
        logging.error(f"Mailgun failed: {e}")
        return False, str(e)

def send_email_ses(to_email, subject, message):
    try:
        response = ses_client.send_email(
            Source='your-email@domain.com',
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}},
            }
        )
        return True, None
    except ClientError as e:
        logging.error(f"AWS SES failed: {e}")
        return False, str(e)
