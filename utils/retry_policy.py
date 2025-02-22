import time
import logging

# Global retry function for all providers
def retry_send(provider_function, retries=4, backoff_factor=2, *args, **kwargs):
    """
    Tries to send the notification using the given provider function with retry and exponential backoff.
    
    provider_function: The function to send the notification (e.g., send_sms, send_email, push_notification).
    eretris: The number of retry attempts.
    backoff_factor: The exponential backoff factor to increase wait time between retries.
    *args, **kwargs: The arguments and keyword arguments to pass to the provider function.
    """
    attempt = 0
    while attempt < retries:
        success, error_message = provider_function(*args, **kwargs)
        if success:
            return True
        else:
            # Exponential backoff
            wait_time = backoff_factor ** attempt
            logging.info(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds.")
            time.sleep(wait_time)
            attempt += 1
    return False
