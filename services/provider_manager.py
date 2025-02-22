from providers.sms_provider import send_sms_twilio, send_sms_sns
from providers.email_provider import send_email_mailgun, send_email_ses
from utils.retry_policy import retry_send
import logging

def send_sms(to_number, message):
    # First, try sending with Twilio
    if retry_send(send_sms_twilio, to_number, message):
        logging.info(f"SMS successfully sent to {to_number} via Twilio.")
        return True

    # If Twilio fails, attempt to send with AWS SNS
    logging.info("Twilio failed, attempting AWS SNS.")
    if retry_send(send_sms_sns, to_number, message):
        logging.info(f"SMS successfully sent to {to_number} via AWS SNS.")
        return True
    
    logging.error(f"Failed to send SMS to {to_number} via both Twilio and AWS SNS.")
    return False


def send_email(to_email, subject, message):
    # First, try sending with Mailgun
    if retry_send(send_email_mailgun, to_email, subject, message):
        logging.info(f"Email successfully sent to {to_email} via Mailgun.")
        return True

    # If Mailgun fails, attempt to send with AWS SES
    logging.info("Mailgun failed, attempting AWS SES.")
    if retry_send(send_email_ses, to_email, subject, message):
        logging.info(f"Email successfully sent to {to_email} via AWS SES.")
        return True
    
    logging.error(f"Failed to send email to {to_email} via both Mailgun and AWS SES.")
    return False